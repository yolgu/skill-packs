#!/usr/bin/env python3
"""Compare the change an old branch carried with the change a rebuilt branch carries.

A rebuilt branch is correct when, file by file, it adds and removes the same lines
as the old branch did. Files listed with --expect are intentional differences
(excluded prototypes, conflict resolutions, moved files) and do not fail the check.

Exit codes: 0 every difference is expected, 1 unexpected differences, 2 git error.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from enum import Enum


class GitError(Exception):
    pass


class Git:
    def __init__(self, repository: str) -> None:
        self.repository: str = repository

    def run(self, *arguments: str) -> str:
        command: list[str] = ["git", "-C", self.repository, "-c", "core.quotePath=false", *arguments]
        result: subprocess.CompletedProcess[str] = subprocess.run(
            command, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if result.returncode != 0:
            raise GitError(f"{' '.join(arguments)}: {result.stderr.strip()}")
        return result.stdout

    def blob_or_none(self, revision: str, path: str) -> str | None:
        try:
            blob: str = self.run("rev-parse", "--verify", "-q", f"{revision}:{path}").strip()
        except GitError:
            return None
        return blob


@dataclass(frozen=True)
class FileChange:
    """Lines one diff adds and removes in a single file, ignoring their positions."""

    path: str
    added: Counter[str]
    removed: Counter[str]
    binary_result_blob: str | None
    is_binary: bool

    def same_change_as(self, other: FileChange) -> bool:
        if self.is_binary or other.is_binary:
            return self.is_binary == other.is_binary and self.binary_result_blob == other.binary_result_blob
        return self.added == other.added and self.removed == other.removed


class Delta:
    """Every file change between a base and a tip, without rename detection."""

    def __init__(self, base: str, tip: str, changes: dict[str, FileChange]) -> None:
        self.base: str = base
        self.tip: str = tip
        self.changes: dict[str, FileChange] = changes

    @classmethod
    def load(cls, git: Git, base: str, tip: str) -> Delta:
        patch: str = git.run("diff", "--no-renames", "--no-color", "--no-ext-diff", "-U0", base, tip)
        changes: dict[str, FileChange] = {}
        for section in cls._split_sections(patch):
            change: FileChange = cls._parse_section(git, tip, section)
            changes[change.path] = change
        return cls(base, tip, changes)

    @staticmethod
    def _split_sections(patch: str) -> list[list[str]]:
        sections: list[list[str]] = []
        for line in patch.splitlines():
            if line.startswith("diff --git "):
                sections.append([line])
            elif sections:
                sections[-1].append(line)
        return sections

    @classmethod
    def _parse_section(cls, git: Git, tip: str, section: list[str]) -> FileChange:
        path: str = cls._path_from_header(section[0])
        added: Counter[str] = Counter()
        removed: Counter[str] = Counter()
        is_binary: bool = False
        # Header lines such as "--- a/x" come before the first hunk. A removed SQL comment
        # also starts with "---", so content is only read once the hunks begin.
        in_hunks: bool = False
        for line in section[1:]:
            if line.startswith("@@"):
                in_hunks = True
            elif not in_hunks:
                is_binary = is_binary or line.startswith("Binary files ")
            elif line.startswith("+"):
                added[line[1:]] += 1
            elif line.startswith("-"):
                removed[line[1:]] += 1
        binary_result_blob: str | None = git.blob_or_none(tip, path) if is_binary else None
        return FileChange(path, added, removed, binary_result_blob, is_binary)

    @staticmethod
    def _path_from_header(header: str) -> str:
        # Without rename detection the header is "diff --git a/<path> b/<path>" with the same path twice.
        both_paths: str = header[len("diff --git a/"):]
        path_length: int = (len(both_paths) - len(" b/")) // 2
        return both_paths[:path_length]


class Verdict(Enum):
    SAME = "같음"
    DIFFERENT = "다름"
    ONLY_OLD = "옛 변경에만 있음"
    ONLY_NEW = "새 변경에만 있음"


@dataclass(frozen=True)
class FileComparison:
    path: str
    verdict: Verdict
    old: FileChange | None
    new: FileChange | None
    expected: bool


class ExpectedPaths:
    """Paths where a difference is intended. An entry ending with '/' covers a directory."""

    def __init__(self, entries: list[str]) -> None:
        self.entries: list[str] = entries

    def covers(self, path: str) -> bool:
        return any(path == entry or (entry.endswith("/") and path.startswith(entry)) for entry in self.entries)


def compare(old: Delta, new: Delta, expected_paths: ExpectedPaths) -> list[FileComparison]:
    comparisons: list[FileComparison] = []
    for path in sorted(set(old.changes) | set(new.changes)):
        old_change: FileChange | None = old.changes.get(path)
        new_change: FileChange | None = new.changes.get(path)
        verdict: Verdict = _verdict(old_change, new_change)
        comparisons.append(FileComparison(path, verdict, old_change, new_change, expected_paths.covers(path)))
    return comparisons


def _verdict(old_change: FileChange | None, new_change: FileChange | None) -> Verdict:
    if new_change is None:
        return Verdict.ONLY_OLD
    if old_change is None:
        return Verdict.ONLY_NEW
    if old_change.same_change_as(new_change):
        return Verdict.SAME
    return Verdict.DIFFERENT


def render(comparisons: list[FileComparison], show_lines: int) -> str:
    same_count: int = sum(1 for comparison in comparisons if comparison.verdict is Verdict.SAME)
    differences: list[FileComparison] = [c for c in comparisons if c.verdict is not Verdict.SAME]
    unexpected_count: int = sum(1 for c in differences if not c.expected)
    output: list[str] = [
        f"파일 {len(comparisons)}개: 같음 {same_count}, 다름 {len(differences)}"
        f" (의도 {len(differences) - unexpected_count}, 확인 필요 {unexpected_count})"
    ]
    for comparison in differences:
        marker: str = "의도" if comparison.expected else "확인 필요"
        output.append(f"[{marker}] {comparison.verdict.value}: {comparison.path} {_line_counts(comparison)}")
        if comparison.verdict is Verdict.DIFFERENT and not comparison.expected and show_lines > 0:
            output.extend(_sample_differences(comparison, show_lines))
    return "\n".join(output)


def _line_counts(comparison: FileComparison) -> str:
    def describe(change: FileChange | None) -> str:
        if change is None:
            return "-"
        if change.is_binary:
            return "binary"
        return f"+{sum(change.added.values())}/-{sum(change.removed.values())}"

    return f"(옛 {describe(comparison.old)}, 새 {describe(comparison.new)})"


def _sample_differences(comparison: FileComparison, limit: int) -> list[str]:
    assert comparison.old is not None and comparison.new is not None
    if comparison.old.is_binary or comparison.new.is_binary:
        return ["    바이너리 결과 파일이 다릅니다"]
    lines: list[str] = []
    groups: list[tuple[str, Counter[str]]] = [
        ("옛 변경만 더한 줄", comparison.old.added - comparison.new.added),
        ("새 변경만 더한 줄", comparison.new.added - comparison.old.added),
        ("옛 변경만 뺀 줄", comparison.old.removed - comparison.new.removed),
        ("새 변경만 뺀 줄", comparison.new.removed - comparison.old.removed),
    ]
    for label, only_one_side in groups:
        for text in list(only_one_side.elements())[:limit]:
            lines.append(f"    {label}: {text.strip()[:140]}")
    return lines


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-C", dest="repository", default=".", help="저장소 경로 (기본: 현재 폴더)")
    parser.add_argument("--old-base", required=True, help="옛 브랜치가 갈라져 나온 지점")
    parser.add_argument("--old-tip", required=True, help="옛 브랜치 끝 (보관 태그 권장)")
    parser.add_argument("--new-base", required=True, help="새 브랜치가 시작한 지점")
    parser.add_argument("--new-tip", required=True, help="새 브랜치 끝")
    parser.add_argument(
        "--expect", action="append", default=[], metavar="PATH",
        help="차이가 의도된 경로. '/'로 끝나면 폴더 전체. 여러 번 줄 수 있다",
    )
    parser.add_argument("--show-lines", type=int, default=5, help="확인 필요 파일마다 보여 줄 다른 줄 수")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    arguments: argparse.Namespace = parse_arguments(argv)
    git: Git = Git(arguments.repository)
    try:
        old: Delta = Delta.load(git, arguments.old_base, arguments.old_tip)
        new: Delta = Delta.load(git, arguments.new_base, arguments.new_tip)
    except GitError as error:
        print(f"git 오류: {error}", file=sys.stderr)
        return 2
    comparisons: list[FileComparison] = compare(old, new, ExpectedPaths(arguments.expect))
    print(render(comparisons, arguments.show_lines))
    has_unexpected: bool = any(c.verdict is not Verdict.SAME and not c.expected for c in comparisons)
    return 1 if has_unexpected else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
