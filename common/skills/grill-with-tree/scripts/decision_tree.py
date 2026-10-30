#!/usr/bin/env python3
"""Read-only operations on a grill-with-tree decision tree.

A tree is one Markdown document, the trunk. Parts split out of it live in a folder next to the trunk
that has the trunk's name, as "<tree name>.<ID>.md" files whose front matter holds root, description,
and parent. A decision is a node line such as "- B.2 [open] Title"; a "선행:" line under a node names
a decision that has to be settled first.

Commands:
  map <tree>           decision map: totals, axes, outline, waiting questions, unconfirmed interpretations
  next <tree>          the next decision to ask: an unsettled prerequisite first, then the shallowest
                       undecided decision in the current axis, then the next axis
  check <tree>         structural problems; never edits the tree
  impact <tree> <ID>   decisions that name <ID> as a prerequisite, mention it, or sit under it

Add --json to any command for machine-readable output.
Exit codes: 0 success (for check: no errors), 1 check found errors, 2 the tree could not be read or the
command was used incorrectly.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

NODE_LINE: re.Pattern[str] = re.compile(
    r"^(?P<indent>[ \t]*)[-*] (?P<id>[A-Z]+(?:\.\d+)*) \[(?P<status>[^\]\n]*)\] (?P<title>\S.*?)\s*$"
)
HEADING_LINE: re.Pattern[str] = re.compile(r"^#{1,6}\s")
STATUS_BLOCK_HEADING: re.Pattern[str] = re.compile(r"^#{1,6}\s+현재 상태\s*$")
POSITION_LINE: re.Pattern[str] = re.compile(r"^\s*(?:[-*]\s+)?작업 위치:\s*(?P<value>.*)$")
DECISION_ID_TOKEN: re.Pattern[str] = re.compile(r"(?<![A-Za-z0-9.])[A-Z]+(?:\.\d+)*(?![A-Za-z0-9]|\.\d)")
LEADING_DECISION_ID: re.Pattern[str] = re.compile(r"^(?P<id>[A-Z]+(?:\.\d+)*)(?![A-Za-z0-9]|\.\d)")
TRAILING_DECISION_ID: re.Pattern[str] = re.compile(r"(?<![A-Za-z0-9])(?P<id>[A-Z]+(?:\.\d+)*)$")
WIKI_LINK_TARGET: re.Pattern[str] = re.compile(r"\[\[(?P<target>[^\]|#]+)")
MARKDOWN_FILE_LINK_TARGET: re.Pattern[str] = re.compile(r"\]\((?P<target>[^)#\s]+?\.md)\)")
RECOMMENDATION_LINE: re.Pattern[str] = re.compile(r"^(?:[^\s(]+\s)?추천\(\d{4}-\d{2}-\d{2}")
LABEL_DATE: re.Pattern[str] = re.compile(r"^\(\d{4}-\d{2}-\d{2}")
LEADING_BULLET: re.Pattern[str] = re.compile(r"^[-*]\s+")

PREREQUISITE_LABEL: str = "선행:"
UNCONFIRMED_INTERPRETATION_LABEL: str = "모델의 해석(사용자 확인 전):"
INTERPRETATION_STEM: str = "모델의 해석"
DATED_LABEL_STEMS: tuple[str, ...] = ("대체됨", "따라 정함", "사용자 결정", "사용자 확인", "추천", "옮김", "부모 철회에 따름")
SPLIT_FILE_FIELDS: tuple[str, ...] = ("root", "description", "parent")


class Status(Enum):
    OPEN = "open"
    BLOCKED = "blocked"
    SETTLED = "settled"
    WITHDRAWN = "withdrawn"

    @classmethod
    def find(cls, word: str) -> Status | None:
        for status in cls:
            if status.value == word:
                return status
        return None


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Location:
    path: Path
    line_number: int

    def describe(self) -> str:
        return f"{self.path.name}:{self.line_number}"


@dataclass(frozen=True)
class Finding:
    severity: Severity
    code: str
    message: str
    location: Location | None


@dataclass(frozen=True)
class Prerequisite:
    """A "선행:" line. node_id is None when the line names no decision ID."""

    node_id: str | None
    text: str
    location: Location


@dataclass(frozen=True)
class FileLink:
    """A line that links to another file of the tree, with the decision it sits under."""

    target_stem: str
    location: Location
    enclosing_node_id: str | None


@dataclass
class DecisionNode:
    node_id: str
    status_word: str
    title: str
    location: Location
    indent: int
    parent_id: str | None
    body: list[tuple[int, str]] = field(default_factory=list)
    prerequisites: list[Prerequisite] = field(default_factory=list)
    children_ids: list[str] = field(default_factory=list)

    @property
    def status(self) -> Status | None:
        return Status.find(self.status_word)

    @property
    def is_undecided(self) -> bool:
        return self.status in (Status.OPEN, Status.BLOCKED)

    def has_recommendation(self) -> bool:
        return any(RECOMMENDATION_LINE.match(text.strip()) for _, text in self.body)

    def unconfirmed_interpretation_lines(self) -> list[tuple[int, str]]:
        return [
            (line_number, text.strip())
            for line_number, text in self.body
            if label_text(text).startswith(UNCONFIRMED_INTERPRETATION_LABEL)
        ]


@dataclass
class TreeFile:
    path: Path
    front_matter: dict[str, str]
    nodes: list[DecisionNode]
    links: list[FileLink]
    status_block: list[tuple[int, str]]
    position_lines: list[tuple[int, str]]


@dataclass
class DecisionTree:
    trunk: Path
    files: list[TreeFile]
    nodes_by_id: dict[str, DecisionNode]
    duplicate_nodes: list[DecisionNode]
    position_id: str | None
    read_findings: list[Finding]

    def find(self, node_id: str) -> DecisionNode | None:
        return self.nodes_by_id.get(node_id)

    def all_nodes(self) -> list[DecisionNode]:
        return sorted(self.nodes_by_id.values(), key=lambda node: id_sort_key(node.node_id))

    def axes(self) -> list[DecisionNode]:
        return [node for node in self.all_nodes() if node.parent_id is None]

    def children_of(self, node: DecisionNode) -> list[DecisionNode]:
        children: list[DecisionNode] = [self.nodes_by_id[child_id] for child_id in node.children_ids]
        return sorted(children, key=lambda child: id_sort_key(child.node_id))

    def ancestors_of(self, node: DecisionNode) -> list[DecisionNode]:
        ancestors: list[DecisionNode] = []
        visited: set[str] = {node.node_id}
        parent_id: str | None = node.parent_id
        while parent_id is not None and parent_id not in visited and parent_id in self.nodes_by_id:
            parent: DecisionNode = self.nodes_by_id[parent_id]
            ancestors.append(parent)
            visited.add(parent_id)
            parent_id = parent.parent_id
        return ancestors

    def depth_of(self, node: DecisionNode) -> int:
        return len(self.ancestors_of(node)) + 1

    def axis_of(self, node: DecisionNode) -> DecisionNode:
        ancestors: list[DecisionNode] = self.ancestors_of(node)
        return ancestors[-1] if ancestors else node

    def breadth_first(self, root: DecisionNode) -> list[DecisionNode]:
        ordered: list[DecisionNode] = []
        queue: deque[DecisionNode] = deque([root])
        visited: set[str] = set()
        while queue:
            node: DecisionNode = queue.popleft()
            if node.node_id in visited:
                continue
            visited.add(node.node_id)
            ordered.append(node)
            queue.extend(self.children_of(node))
        return ordered

    def descendants_of(self, node: DecisionNode) -> list[DecisionNode]:
        return self.breadth_first(node)[1:]


def id_sort_key(node_id: str) -> tuple[int, str, tuple[int, ...]]:
    parts: list[str] = node_id.split(".")
    numbers: tuple[int, ...] = tuple(int(part) for part in parts[1:])
    return (len(parts[0]), parts[0], numbers)


def indent_width(whitespace: str) -> int:
    return len(whitespace.expandtabs(4))


def label_text(line: str) -> str:
    """The line without indentation or a leading bullet, where label words begin."""
    return LEADING_BULLET.sub("", line.strip(), count=1)


def mention_pattern(node_id: str) -> re.Pattern[str]:
    return re.compile(rf"(?<![A-Za-z0-9.]){re.escape(node_id)}(?![A-Za-z0-9]|\.\d)")


def decision_id_in_reference(reference: str) -> str | None:
    """The decision a "선행:" line names, written as an ID or as a wikilink to "<tree>.<ID>"."""
    wiki_match: re.Match[str] | None = WIKI_LINK_TARGET.search(reference)
    if wiki_match is not None:
        trailing: re.Match[str] | None = TRAILING_DECISION_ID.search(wiki_match.group("target").strip())
        return trailing.group("id") if trailing is not None else None
    leading: re.Match[str] | None = LEADING_DECISION_ID.match(reference.strip())
    return leading.group("id") if leading is not None else None


def link_target_stems(line: str) -> list[str]:
    wiki_targets: list[str] = [Path(match.group("target").strip()).name for match in WIKI_LINK_TARGET.finditer(line)]
    file_targets: list[str] = [Path(match.group("target")).stem for match in MARKDOWN_FILE_LINK_TARGET.finditer(line)]
    return [target[:-3] if target.endswith(".md") else target for target in wiki_targets + file_targets]


class TreeReader:
    """Reads a trunk document and its split files. Unknown lines are ignored, so old trees still read."""

    def read(self, trunk: Path) -> DecisionTree:
        paths: list[Path] = [trunk, *self._split_file_paths(trunk)]
        files: list[TreeFile] = [self._read_file(path) for path in paths]
        nodes_by_id: dict[str, DecisionNode] = {}
        duplicate_nodes: list[DecisionNode] = []
        for tree_file in files:
            for node in tree_file.nodes:
                if node.node_id in nodes_by_id:
                    duplicate_nodes.append(node)
                else:
                    nodes_by_id[node.node_id] = node
        tree: DecisionTree = DecisionTree(
            trunk=trunk,
            files=files,
            nodes_by_id=nodes_by_id,
            duplicate_nodes=duplicate_nodes,
            position_id=self._position_id(files[0], nodes_by_id),
            read_findings=[],
        )
        self._resolve_split_file_parents(tree)
        self._link_children(tree)
        return tree

    def _split_file_paths(self, trunk: Path) -> list[Path]:
        folder: Path = trunk.parent / trunk.stem
        return sorted(folder.glob("*.md")) if folder.is_dir() else []

    def _read_file(self, path: Path) -> TreeFile:
        lines: list[str] = path.read_text(encoding="utf-8").splitlines()
        front_matter: dict[str, str]
        start: int
        front_matter, start = self._front_matter(lines)
        nodes: list[DecisionNode] = []
        links: list[FileLink] = []
        status_block: list[tuple[int, str]] = []
        position_lines: list[tuple[int, str]] = []
        open_nodes: list[DecisionNode] = []
        current: DecisionNode | None = None
        in_status_block: bool = False
        for index in range(start, len(lines)):
            line: str = lines[index]
            line_number: int = index + 1
            location: Location = Location(path, line_number)
            if POSITION_LINE.match(line):
                position_lines.append((line_number, line))
            node_match: re.Match[str] | None = NODE_LINE.match(line)
            if node_match is not None:
                indent: int = indent_width(node_match.group("indent"))
                while open_nodes and open_nodes[-1].indent >= indent:
                    open_nodes.pop()
                node: DecisionNode = DecisionNode(
                    node_id=node_match.group("id"),
                    status_word=node_match.group("status").strip(),
                    title=node_match.group("title"),
                    location=location,
                    indent=indent,
                    parent_id=open_nodes[-1].node_id if open_nodes else None,
                )
                nodes.append(node)
                open_nodes.append(node)
                current = node
                continue
            if HEADING_LINE.match(line):
                in_status_block = STATUS_BLOCK_HEADING.match(line) is not None
                open_nodes.clear()
                current = None
                continue
            if in_status_block:
                status_block.append((line_number, line))
            line_indent: int = indent_width(line[: len(line) - len(line.lstrip())])
            enclosing: list[DecisionNode] = [node for node in open_nodes if node.indent < line_indent]
            for target in link_target_stems(line):
                links.append(FileLink(target, location, enclosing[-1].node_id if enclosing else None))
            if current is None:
                continue
            current.body.append((line_number, line))
            text: str = label_text(line)
            if text.startswith(PREREQUISITE_LABEL):
                reference: str = text[len(PREREQUISITE_LABEL):]
                current.prerequisites.append(Prerequisite(decision_id_in_reference(reference), text, location))
        return TreeFile(path, front_matter, nodes, links, status_block, position_lines)

    def _front_matter(self, lines: list[str]) -> tuple[dict[str, str], int]:
        if not lines or lines[0].strip() != "---":
            return {}, 0
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                fields: dict[str, str] = {}
                for raw in lines[1:index]:
                    key: str
                    separator: str
                    value: str
                    key, separator, value = raw.partition(":")
                    if separator:
                        fields[key.strip()] = value.strip().strip('"').strip("'")
                return fields, index + 1
        return {}, 0

    def _position_id(self, trunk_file: TreeFile, nodes_by_id: dict[str, DecisionNode]) -> str | None:
        """The first decision ID on the 작업 위치 line: the one in the 현재 상태 block, else the last one."""
        status_block_numbers: set[int] = {line_number for line_number, _ in trunk_file.status_block}
        in_block: list[tuple[int, str]] = [entry for entry in trunk_file.position_lines if entry[0] in status_block_numbers]
        candidates: list[tuple[int, str]] = in_block[:1] if in_block else trunk_file.position_lines[-1:]
        for _, line in candidates:
            position_match: re.Match[str] | None = POSITION_LINE.match(line)
            value: str = position_match.group("value") if position_match is not None else ""
            tokens: list[str] = DECISION_ID_TOKEN.findall(value)
            known: list[str] = [token for token in tokens if token in nodes_by_id]
            if known or tokens:
                return (known or tokens)[0]
        return None

    def _resolve_split_file_parents(self, tree: DecisionTree) -> None:
        files_by_stem: dict[str, TreeFile] = {tree_file.path.stem: tree_file for tree_file in tree.files}
        for tree_file in tree.files[1:]:
            missing_fields: list[str] = [name for name in SPLIT_FILE_FIELDS if not tree_file.front_matter.get(name)]
            if missing_fields:
                tree.read_findings.append(Finding(
                    Severity.ERROR, "front-matter",
                    f"split file is missing front matter field(s): {', '.join(missing_fields)}",
                    Location(tree_file.path, 1),
                ))
            if not tree_file.nodes:
                continue
            root: DecisionNode = tree_file.nodes[0]
            declared_root: str = tree_file.front_matter.get("root", "")
            if declared_root and declared_root != root.node_id:
                tree.read_findings.append(Finding(
                    Severity.ERROR, "front-matter",
                    f"root is {declared_root} but the file's first decision is {root.node_id}",
                    Location(tree_file.path, 1),
                ))
            parent_stems: list[str] = link_target_stems(tree_file.front_matter.get("parent", ""))
            parent_file: TreeFile | None = files_by_stem.get(parent_stems[0]) if parent_stems else None
            for node in tree_file.nodes:
                if node.parent_id is None:
                    node.parent_id = self._parent_from_link(node, tree_file, parent_file, tree)

    def _parent_from_link(
        self, node: DecisionNode, tree_file: TreeFile, parent_file: TreeFile | None, tree: DecisionTree
    ) -> str | None:
        if parent_file is not None:
            for link in parent_file.links:
                if link.target_stem == tree_file.path.stem:
                    return link.enclosing_node_id
        tree.read_findings.append(Finding(
            Severity.ERROR, "front-matter",
            f"no link line to this file was found in its parent file; {node.node_id} is placed by its ID",
            node.location,
        ))
        parent_by_id: str = node.node_id.rpartition(".")[0]
        return parent_by_id if parent_by_id in tree.nodes_by_id else None

    def _link_children(self, tree: DecisionTree) -> None:
        for node in tree.all_nodes():
            parent: DecisionNode | None = tree.find(node.parent_id) if node.parent_id is not None else None
            if parent is not None:
                parent.children_ids.append(node.node_id)


@dataclass(frozen=True)
class NextDecision:
    node: DecisionNode | None
    reasons: list[str]


class NextDecisionFinder:
    """The question order: an unsettled prerequisite first, then the shallowest undecided decision in the
    current axis (siblings before children), then the next axis."""

    def __init__(self, tree: DecisionTree) -> None:
        self.tree: DecisionTree = tree

    def find(self, position_id: str | None) -> NextDecision:
        axes: list[DecisionNode] = self.tree.axes()
        if not axes:
            return NextDecision(None, ["the tree has no decision nodes"])
        reasons: list[str] = []
        start_index: int = 0
        position: DecisionNode | None = self.tree.find(position_id) if position_id is not None else None
        if position is not None:
            start_axis: DecisionNode = self.tree.axis_of(position)
            start_index = [axis.node_id for axis in axes].index(start_axis.node_id)
            reasons.append(f"current position is {position_id}, so the search starts in axis {start_axis.node_id}")
        elif position_id is not None:
            reasons.append(f"position {position_id} is not a decision in this tree; the search starts in axis {axes[0].node_id}")
        for offset in range(len(axes)):
            axis: DecisionNode = axes[(start_index + offset) % len(axes)]
            for candidate in self.tree.breadth_first(axis):
                if not candidate.is_undecided:
                    continue
                target: DecisionNode | None
                chain: list[str]
                target, chain = self._answerable_from(candidate, set())
                if target is not None:
                    found: list[str] = [f"{candidate.node_id} is the shallowest undecided decision in axis {axis.node_id}"]
                    return NextDecision(target, reasons + found + chain + [f"ask {target.node_id}"])
            reasons.append(f"axis {axis.node_id} has no decision that can be answered now")
        undecided: list[DecisionNode] = [node for node in self.tree.all_nodes() if node.is_undecided]
        if not undecided:
            return NextDecision(None, reasons + ["every decision is settled or withdrawn"])
        blocked_ids: str = ", ".join(node.node_id for node in undecided)
        return NextDecision(None, reasons + [f"only decisions that cannot be answered now remain: {blocked_ids}"])

    def _answerable_from(self, node: DecisionNode, visiting: set[str]) -> tuple[DecisionNode | None, list[str]]:
        if node.node_id in visiting:
            return None, [f"{node.node_id} is part of a prerequisite cycle"]
        visiting.add(node.node_id)
        prerequisites: list[DecisionNode] = [
            prerequisite for prerequisite in self._prerequisite_nodes(node) if prerequisite.status is not Status.SETTLED
        ]
        answerable_prerequisites: list[DecisionNode] = [prerequisite for prerequisite in prerequisites if prerequisite.is_undecided]
        unusable_references: bool = len(answerable_prerequisites) < len(prerequisites) or self._has_missing_prerequisite(node)
        if not prerequisites and not unusable_references:
            if node.status is Status.BLOCKED:
                return node, [f"{node.node_id} is marked blocked but every prerequisite is settled; change it to open"]
            return node, []
        for prerequisite in answerable_prerequisites:
            target: DecisionNode | None
            notes: list[str]
            target, notes = self._answerable_from(prerequisite, visiting)
            if target is not None:
                return target, [f"{node.node_id} waits on {prerequisite.node_id} (선행)"] + notes
        return None, [f"{node.node_id} waits on prerequisites that cannot be answered now"]

    def _prerequisite_nodes(self, node: DecisionNode) -> list[DecisionNode]:
        found: list[DecisionNode | None] = [
            self.tree.find(prerequisite.node_id) for prerequisite in node.prerequisites if prerequisite.node_id is not None
        ]
        return [prerequisite for prerequisite in found if prerequisite is not None]

    def _has_missing_prerequisite(self, node: DecisionNode) -> bool:
        return any(prerequisite.node_id is None or self.tree.find(prerequisite.node_id) is None for prerequisite in node.prerequisites)


@dataclass(frozen=True)
class ImpactEntry:
    node: DecisionNode
    reasons: list[str]
    line_numbers: list[int]


@dataclass(frozen=True)
class Impact:
    target: DecisionNode
    entries: list[ImpactEntry]
    status_block_mentions: list[Location]


def find_impact(tree: DecisionTree, target: DecisionNode) -> Impact:
    pattern: re.Pattern[str] = mention_pattern(target.node_id)
    descendant_ids: set[str] = {node.node_id for node in tree.descendants_of(target)}
    entries: list[ImpactEntry] = []
    for node in tree.all_nodes():
        if node is target:
            continue
        reasons: list[str] = []
        line_numbers: list[int] = []
        prerequisite_lines: list[int] = [
            prerequisite.location.line_number for prerequisite in node.prerequisites if prerequisite.node_id == target.node_id
        ]
        if prerequisite_lines:
            reasons.append("prerequisite")
            line_numbers.extend(prerequisite_lines)
        mention_lines: list[int] = [
            line_number for line_number, text in node.body
            if pattern.search(text) and not label_text(text).startswith(PREREQUISITE_LABEL)
        ]
        if mention_lines:
            reasons.append("mention")
            line_numbers.extend(mention_lines)
        if node.node_id in descendant_ids:
            reasons.append("descendant")
        if reasons:
            entries.append(ImpactEntry(node, reasons, sorted(line_numbers)))
    trunk_file: TreeFile = tree.files[0]
    status_block_mentions: list[Location] = [
        Location(trunk_file.path, line_number) for line_number, text in trunk_file.status_block if pattern.search(text)
    ]
    return Impact(target, entries, status_block_mentions)


class TreeChecker:
    """Structural checks that are deterministic and easy to get wrong by hand. Never edits the tree."""

    def __init__(self, tree: DecisionTree) -> None:
        self.tree: DecisionTree = tree

    def check(self) -> list[Finding]:
        findings: list[Finding] = list(self.tree.read_findings)
        findings.extend(self._duplicate_ids())
        findings.extend(self._unknown_statuses())
        findings.extend(self._prerequisite_targets())
        findings.extend(self._prerequisite_cycles())
        findings.extend(self._statuses_against_prerequisites())
        findings.extend(self._label_formats())
        return findings

    def _duplicate_ids(self) -> list[Finding]:
        return [
            Finding(
                Severity.ERROR, "duplicate-id",
                f"{node.node_id} is already used at {self.tree.nodes_by_id[node.node_id].location.describe()}",
                node.location,
            )
            for node in self.tree.duplicate_nodes
        ]

    def _unknown_statuses(self) -> list[Finding]:
        allowed: str = ", ".join(status.value for status in Status)
        return [
            Finding(Severity.ERROR, "unknown-status", f"{node.node_id} has status '{node.status_word}'; use one of {allowed}", node.location)
            for node in self._every_node()
            if node.status is None
        ]

    def _prerequisite_targets(self) -> list[Finding]:
        findings: list[Finding] = []
        for node in self._every_node():
            for prerequisite in node.prerequisites:
                if prerequisite.node_id is None:
                    findings.append(Finding(
                        Severity.ERROR, "prerequisite-format",
                        f"the 선행: line under {node.node_id} names no decision ID: '{prerequisite.text}'",
                        prerequisite.location,
                    ))
                elif self.tree.find(prerequisite.node_id) is None:
                    findings.append(Finding(
                        Severity.ERROR, "missing-prerequisite",
                        f"{node.node_id} names {prerequisite.node_id} as a prerequisite, but no such decision exists",
                        prerequisite.location,
                    ))
        return findings

    def _prerequisite_cycles(self) -> list[Finding]:
        findings: list[Finding] = []
        reported: set[tuple[str, ...]] = set()
        for start in self.tree.all_nodes():
            for cycle in self._cycles_from(start.node_id, [start.node_id]):
                rotation: int = cycle.index(min(cycle, key=id_sort_key))
                canonical: tuple[str, ...] = tuple(cycle[rotation:] + cycle[:rotation])
                if canonical in reported:
                    continue
                reported.add(canonical)
                findings.append(Finding(
                    Severity.ERROR, "prerequisite-cycle",
                    "prerequisites form a cycle: " + " -> ".join(canonical + (canonical[0],)),
                    self.tree.nodes_by_id[canonical[0]].location,
                ))
        return findings

    def _cycles_from(self, node_id: str, path: list[str]) -> list[list[str]]:
        cycles: list[list[str]] = []
        node: DecisionNode | None = self.tree.find(node_id)
        if node is None:
            return cycles
        for prerequisite in node.prerequisites:
            next_id: str | None = prerequisite.node_id
            if next_id is None or self.tree.find(next_id) is None:
                continue
            if next_id == path[0]:
                cycles.append(list(path))
            elif next_id not in path and id_sort_key(next_id) > id_sort_key(path[0]):
                cycles.extend(self._cycles_from(next_id, path + [next_id]))
        return cycles

    def _statuses_against_prerequisites(self) -> list[Finding]:
        findings: list[Finding] = []
        for node in self.tree.all_nodes():
            known: list[DecisionNode] = [
                self.tree.nodes_by_id[prerequisite.node_id]
                for prerequisite in node.prerequisites
                if prerequisite.node_id is not None and prerequisite.node_id in self.tree.nodes_by_id
            ]
            unsettled: list[DecisionNode] = [prerequisite for prerequisite in known if prerequisite.status is not Status.SETTLED]
            if node.status is Status.OPEN and unsettled:
                names: str = ", ".join(f"{prerequisite.node_id} ({prerequisite.status_word})" for prerequisite in unsettled)
                findings.append(Finding(
                    Severity.ERROR, "status-mismatch",
                    f"{node.node_id} is open but waits on {names}; mark it blocked, or update the 선행: line if that premise is gone",
                    node.location,
                ))
            if node.status is Status.BLOCKED and not node.prerequisites:
                findings.append(Finding(
                    Severity.ERROR, "status-mismatch",
                    f"{node.node_id} is blocked but has no 선행: line; add the prerequisite or mark it open",
                    node.location,
                ))
            elif node.status is Status.BLOCKED and known and not unsettled and len(known) == len(node.prerequisites):
                findings.append(Finding(
                    Severity.ERROR, "status-mismatch",
                    f"{node.node_id} is blocked but every prerequisite is settled; mark it open",
                    node.location,
                ))
        return findings

    def _label_formats(self) -> list[Finding]:
        """Warnings, not errors: labels other than 선행: carry meaning for people but not for reading the tree."""
        findings: list[Finding] = []
        for node in self._every_node():
            for line_number, line in node.body:
                problem: str | None = label_problem(label_text(line))
                if problem is not None:
                    findings.append(Finding(Severity.WARNING, "label-format", f"under {node.node_id}: {problem}", Location(node.location.path, line_number)))
        return findings

    def _every_node(self) -> list[DecisionNode]:
        return self.tree.all_nodes() + self.tree.duplicate_nodes


def label_problem(text: str) -> str | None:
    """Why a label line breaks the literal label format, or None when it is fine or is not a label line."""
    if text.startswith(INTERPRETATION_STEM) and text[len(INTERPRETATION_STEM):][:1] in ("(", ":"):
        if not text.startswith(UNCONFIRMED_INTERPRETATION_LABEL):
            return f"write an unconfirmed interpretation as '{UNCONFIRMED_INTERPRETATION_LABEL}', or relabel it '사용자 확인(YYYY-MM-DD):' once confirmed"
        return None
    for stem in DATED_LABEL_STEMS:
        rest: str = text[len(stem):]
        if text.startswith(stem) and rest[:1] in ("(", ":") and LABEL_DATE.match(rest) is None:
            return f"'{stem}' needs a date right after it, as '{stem}(YYYY-MM-DD…)'"
    return None


@dataclass(frozen=True)
class AxisSummary:
    axis: DecisionNode
    decision_count: int
    status_counts: dict[str, int]
    max_depth: int


@dataclass(frozen=True)
class TreeMap:
    tree: DecisionTree
    status_counts: dict[str, int]
    axes: list[AxisSummary]
    outline: list[tuple[int, DecisionNode]]
    waiting_questions: list[DecisionNode]
    unconfirmed_interpretations: list[tuple[DecisionNode, int, str]]


def build_map(tree: DecisionTree) -> TreeMap:
    axes: list[AxisSummary] = []
    outline: list[tuple[int, DecisionNode]] = []
    for axis in tree.axes():
        members: list[DecisionNode] = tree.breadth_first(axis)
        axes.append(AxisSummary(
            axis=axis,
            decision_count=len(members),
            status_counts=count_statuses(members),
            max_depth=max(tree.depth_of(member) for member in members),
        ))
        outline.extend(depth_first_outline(tree, axis, 1))
    return TreeMap(
        tree=tree,
        status_counts=count_statuses(tree.all_nodes()),
        axes=axes,
        outline=outline,
        waiting_questions=[node for node in tree.all_nodes() if node.is_undecided and node.has_recommendation()],
        unconfirmed_interpretations=[
            (node, line_number, text) for node in tree.all_nodes() for line_number, text in node.unconfirmed_interpretation_lines()
        ],
    )


def depth_first_outline(tree: DecisionTree, node: DecisionNode, depth: int) -> list[tuple[int, DecisionNode]]:
    lines: list[tuple[int, DecisionNode]] = [(depth, node)]
    for child in tree.children_of(node):
        lines.extend(depth_first_outline(tree, child, depth + 1))
    return lines


def count_statuses(nodes: list[DecisionNode]) -> dict[str, int]:
    counts: dict[str, int] = {status.value: 0 for status in Status}
    for node in nodes:
        counts[node.status_word] = counts.get(node.status_word, 0) + 1
    return counts


def format_counts(counts: dict[str, int]) -> str:
    return ", ".join(f"{word} {count}" for word, count in counts.items() if count)


def node_label(node: DecisionNode) -> str:
    return f"{node.node_id} [{node.status_word}] {node.title}"


def node_json(node: DecisionNode) -> dict[str, object]:
    return {
        "id": node.node_id,
        "status": node.status_word,
        "title": node.title,
        "parent": node.parent_id,
        "location": node.location.describe(),
        "prerequisites": [prerequisite.node_id for prerequisite in node.prerequisites],
    }


def finding_json(finding: Finding) -> dict[str, object]:
    return {
        "severity": finding.severity.value,
        "code": finding.code,
        "message": finding.message,
        "location": finding.location.describe() if finding.location is not None else None,
    }


def render_map(tree_map: TreeMap) -> str:
    tree: DecisionTree = tree_map.tree
    total: int = sum(tree_map.status_counts.values())
    lines: list[str] = [f"tree: {tree.trunk} ({len(tree.files)} file(s))", f"position: {tree.position_id or 'none'}"]
    lines.append(f"decisions: {total} ({format_counts(tree_map.status_counts)})")
    lines.append("axes:")
    for summary in tree_map.axes:
        lines.append(
            f"  {node_label(summary.axis)} - {summary.decision_count} decision(s) "
            f"({format_counts(summary.status_counts)}), depth {summary.max_depth}"
        )
    lines.append("outline:")
    for depth, node in tree_map.outline:
        prerequisites: list[str] = [prerequisite.node_id or "?" for prerequisite in node.prerequisites]
        suffix: str = f"  (선행: {', '.join(prerequisites)})" if prerequisites else ""
        lines.append(f"{'  ' * depth}{node_label(node)}{suffix}")
    lines.append("waiting questions (undecided, with a 추천 line):")
    lines.extend(f"  {node_label(node)}" for node in tree_map.waiting_questions)
    if not tree_map.waiting_questions:
        lines.append("  none")
    lines.append("unconfirmed interpretation lines (judge whether each is still live):")
    lines.extend(f"  {node.node_id} line {line_number}: {text}" for node, line_number, text in tree_map.unconfirmed_interpretations)
    if not tree_map.unconfirmed_interpretations:
        lines.append("  none")
    if len(tree.files) > 1:
        lines.append("files:")
        for tree_file in tree.files[1:]:
            front_matter: dict[str, str] = tree_file.front_matter
            lines.append(
                f"  {tree_file.path.name}: root {front_matter.get('root', '?')}, parent {front_matter.get('parent', '?')}, "
                f"{front_matter.get('description', '')}"
            )
    return "\n".join(lines)


def map_json(tree_map: TreeMap) -> dict[str, object]:
    tree: DecisionTree = tree_map.tree
    return {
        "tree": str(tree.trunk),
        "position": tree.position_id,
        "status_counts": tree_map.status_counts,
        "axes": [
            {
                "id": summary.axis.node_id,
                "title": summary.axis.title,
                "status": summary.axis.status_word,
                "decision_count": summary.decision_count,
                "status_counts": summary.status_counts,
                "max_depth": summary.max_depth,
            }
            for summary in tree_map.axes
        ],
        "outline": [{"depth": depth, **node_json(node)} for depth, node in tree_map.outline],
        "waiting_questions": [node.node_id for node in tree_map.waiting_questions],
        "unconfirmed_interpretations": [
            {"id": node.node_id, "line": line_number, "text": text} for node, line_number, text in tree_map.unconfirmed_interpretations
        ],
        "files": [{"path": str(tree_file.path), **tree_file.front_matter} for tree_file in tree.files[1:]],
    }


def render_next(next_decision: NextDecision) -> str:
    head: str = f"next: {node_label(next_decision.node)}" if next_decision.node is not None else "next: none"
    return "\n".join([head, *[f"  - {reason}" for reason in next_decision.reasons]])


def render_findings(findings: list[Finding]) -> str:
    errors: int = sum(1 for finding in findings if finding.severity is Severity.ERROR)
    lines: list[str] = [
        f"{finding.severity.value} {finding.code} {finding.location.describe() if finding.location else '-'}: {finding.message}"
        for finding in findings
    ]
    lines.append(f"{errors} error(s), {len(findings) - errors} warning(s)")
    return "\n".join(lines)


def render_impact(impact: Impact) -> str:
    lines: list[str] = [f"impact of {node_label(impact.target)}:"]
    for entry in impact.entries:
        where: str = f" at line(s) {', '.join(str(number) for number in entry.line_numbers)}" if entry.line_numbers else ""
        lines.append(f"  {node_label(entry.node)} - {', '.join(entry.reasons)}{where}")
    if not impact.entries:
        lines.append("  no decision depends on, mentions, or sits under it")
    for location in impact.status_block_mentions:
        lines.append(f"  현재 상태 block mentions it at {location.describe()}")
    return "\n".join(lines)


def impact_json(impact: Impact) -> dict[str, object]:
    return {
        "target": node_json(impact.target),
        "entries": [
            {**node_json(entry.node), "reasons": entry.reasons, "lines": entry.line_numbers} for entry in impact.entries
        ],
        "status_block_mentions": [location.describe() for location in impact.status_block_mentions],
    }


def build_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Read-only operations on a grill-with-tree decision tree."
    )
    commands: argparse._SubParsersAction[argparse.ArgumentParser] = parser.add_subparsers(dest="command", required=True)
    for name, summary in (("map", "decision map"), ("next", "next decision to ask"), ("check", "structural problems")):
        command: argparse.ArgumentParser = commands.add_parser(name, help=summary)
        command.add_argument("tree", type=Path, help="the trunk document")
        command.add_argument("--json", action="store_true", help="machine-readable output")
        if name == "next":
            command.add_argument("--from", dest="position", help="start from this decision instead of 작업 위치")
    impact_command: argparse.ArgumentParser = commands.add_parser("impact", help="decisions affected by a decision")
    impact_command.add_argument("tree", type=Path, help="the trunk document")
    impact_command.add_argument("node_id", help="the decision ID, such as B.2")
    impact_command.add_argument("--json", action="store_true", help="machine-readable output")
    return parser


def emit(text: str, payload: dict[str, object], as_json: bool) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2) if as_json else text)


def main(argv: list[str] | None = None) -> int:
    arguments: argparse.Namespace = build_parser().parse_args(argv)
    try:
        tree: DecisionTree = TreeReader().read(arguments.tree)
    except (OSError, UnicodeDecodeError) as error:
        print(f"cannot read the tree: {error}", file=sys.stderr)
        return 2
    if arguments.command == "map":
        tree_map: TreeMap = build_map(tree)
        emit(render_map(tree_map), map_json(tree_map), arguments.json)
        return 0
    if arguments.command == "next":
        next_decision: NextDecision = NextDecisionFinder(tree).find(arguments.position or tree.position_id)
        payload: dict[str, object] = {
            "next": node_json(next_decision.node) if next_decision.node is not None else None,
            "reasons": next_decision.reasons,
        }
        emit(render_next(next_decision), payload, arguments.json)
        return 0
    if arguments.command == "check":
        findings: list[Finding] = TreeChecker(tree).check()
        emit(render_findings(findings), {"findings": [finding_json(finding) for finding in findings]}, arguments.json)
        return 1 if any(finding.severity is Severity.ERROR for finding in findings) else 0
    target: DecisionNode | None = tree.find(arguments.node_id)
    if target is None:
        print(f"no decision {arguments.node_id} in {arguments.tree}", file=sys.stderr)
        return 2
    impact: Impact = find_impact(tree, target)
    emit(render_impact(impact), impact_json(impact), arguments.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
