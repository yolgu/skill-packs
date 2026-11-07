"""Build a self-contained five-choice concept quiz page from a quiz JSON file.

Usage:
    python3 build_quiz.py <quiz.json> <output.html> [--fragment <fragment.html>]

The output page splits the questions into sets of `set_size` (default 5) with a
bottom bar for retrying the current set, showing wrong answers only, and moving to
the next set. `--fragment` also writes the bare widget for an inline chat widget.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass
from pathlib import Path

OPTION_COUNT: int = 5
DEFAULT_SET_SIZE: int = 5
TEMPLATE_PATH: Path = Path(__file__).resolve().parent.parent / "assets" / "quiz-widget.html"
QUESTION_FIELDS: tuple[str, ...] = ("s", "q", "o", "a", "e", "l", "t")
TEXT_FIELDS: tuple[str, ...] = ("q", "e", "t")
# The widget prints text literally, so TeX-style `x^n` or `a_i` shows up raw on screen.
ASCII_MATH: re.Pattern[str] = re.compile(r"[A-Za-z0-9)][\^_][A-Za-z0-9({]")


class QuizFormatError(ValueError):
    """The quiz JSON does not match the format the widget renders."""


@dataclass(frozen=True)
class Quiz:
    title: str
    summary: str
    sections: list[str]
    questions: list[dict[str, object]]
    set_size: int

    @classmethod
    def from_json(cls, raw: dict[str, object]) -> Quiz:
        sections: list[str] = list(raw.get("sections") or [])
        questions: list[dict[str, object]] = list(raw.get("questions") or [])
        set_size: int = int(raw.get("set_size") or DEFAULT_SET_SIZE)
        if not sections:
            raise QuizFormatError("sections must list at least one section name")
        if not questions:
            raise QuizFormatError("questions must not be empty")
        for number, question in enumerate(questions, start=1):
            cls._check_question(number, question, len(sections))
        return cls(
            title=str(raw["title"]),
            summary=str(raw.get("summary") or raw["title"]),
            sections=sections,
            questions=questions,
            set_size=set_size,
        )

    @staticmethod
    def _check_question(number: int, question: dict[str, object], section_count: int) -> None:
        missing: list[str] = [field for field in QUESTION_FIELDS if field not in question]
        if missing:
            raise QuizFormatError(f"question {number} is missing {missing}")
        options: list[str] = list(question["o"])  # type: ignore[arg-type]
        if len(options) != OPTION_COUNT or len(set(options)) != OPTION_COUNT:
            raise QuizFormatError(f"question {number} needs {OPTION_COUNT} distinct options")
        if not 0 <= int(question["a"]) < OPTION_COUNT:  # type: ignore[arg-type]
            raise QuizFormatError(f"question {number} answer index must be 0-{OPTION_COUNT - 1}")
        if not 0 <= int(question["s"]) < section_count:  # type: ignore[arg-type]
            raise QuizFormatError(f"question {number} section index is out of range")

    def answer_positions(self) -> list[int]:
        positions: list[int] = [0] * OPTION_COUNT
        for question in self.questions:
            positions[int(question["a"])] += 1  # type: ignore[arg-type]
        return positions

    def ascii_math_warnings(self) -> list[str]:
        warnings: list[str] = []
        for number, question in enumerate(self.questions, start=1):
            texts: list[str] = [str(question[field]) for field in TEXT_FIELDS] + list(question["o"])  # type: ignore[arg-type]
            for text in texts:
                prose: str = "".join(text.split("`")[0::2])
                for match in ASCII_MATH.finditer(prose):
                    warnings.append(f"question {number}: '{match.group(0)}' in “{text[:40]}…”")
        return warnings

    def render_widget(self) -> str:
        numbered: list[dict[str, object]] = [
            {"n": number, **{field: question[field] for field in QUESTION_FIELDS}}
            for number, question in enumerate(self.questions, start=1)
        ]
        template: str = TEMPLATE_PATH.read_text(encoding="utf-8")
        return (
            template.replace("__QUIZ_SUMMARY__", html.escape(self.summary))
            .replace("__QUIZ_SET_SIZE__", str(self.set_size))
            .replace("__QUIZ_SECTIONS__", _script_json(self.sections))
            .replace("__QUIZ_QUESTIONS__", _script_json(numbered))
        )

    def render_page(self, widget: str) -> str:
        title: str = html.escape(self.title)
        return (
            '<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f"<title>{title}</title>\n"
            "<style>body{margin:0 auto;max-width:760px;padding-block:24px;"
            "padding-left:max(16px,env(safe-area-inset-left,0px));"
            "padding-right:max(16px,env(safe-area-inset-right,0px));"
            "background:#ffffff;font-family:system-ui,-apple-system,sans-serif}"
            "h1{font-size:20px;margin:0 0 16px;color:#1f1e1d}</style>\n"
            f"</head>\n<body>\n<h1>{title}</h1>\n{widget}</body>\n</html>\n"
        )


def _script_json(value: object) -> str:
    # Escaping "<" keeps a "</script>" inside question text from closing the script tag.
    return json.dumps(value, ensure_ascii=False).replace("<", "\\u003c")


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("quiz_json", type=Path)
    parser.add_argument("output_html", type=Path)
    parser.add_argument("--fragment", type=Path, help="also write the bare widget for an inline chat widget")
    args: argparse.Namespace = parser.parse_args()

    quiz: Quiz = Quiz.from_json(json.loads(args.quiz_json.read_text(encoding="utf-8")))
    widget: str = quiz.render_widget()
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(quiz.render_page(widget), encoding="utf-8")
    if args.fragment:
        args.fragment.write_text(widget, encoding="utf-8")

    set_count: int = -(-len(quiz.questions) // quiz.set_size)
    print(f"questions {len(quiz.questions)} in {set_count} set(s) of {quiz.set_size}")
    print(f"answer positions ①-⑤: {quiz.answer_positions()}")
    if len(quiz.questions) % quiz.set_size:
        print(f"WARNING last set has only {len(quiz.questions) % quiz.set_size} question(s); use a multiple of {quiz.set_size}")
    for warning in quiz.ascii_math_warnings():
        print(f"WARNING ascii math (use Unicode sub/superscripts): {warning}")
    print(f"wrote {args.output_html}")


if __name__ == "__main__":
    main()
