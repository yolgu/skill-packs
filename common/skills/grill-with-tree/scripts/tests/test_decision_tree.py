"""Behavior of the read-only tree commands, checked against fictional trees in fixtures/."""

from __future__ import annotations

import io
import json
import sys
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SCRIPTS_DIR: Path = Path(__file__).resolve().parent.parent
FIXTURES: Path = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SCRIPTS_DIR))

import decision_tree as dt  # noqa: E402  (the script lives one folder up and is not a package)


def read_fixture(name: str) -> dt.DecisionTree:
    return dt.TreeReader().read(FIXTURES / name)


def write_tree(folder: Path, name: str, body: str) -> Path:
    path: Path = folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(body).lstrip("\n"), encoding="utf-8")
    return path


def run_main(arguments: list[str]) -> tuple[int, str, str]:
    stdout: io.StringIO = io.StringIO()
    stderr: io.StringIO = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        exit_code: int = dt.main(arguments)
    return exit_code, stdout.getvalue(), stderr.getvalue()


class ReadingTest(unittest.TestCase):
    def test_single_document_reads_nodes_parents_and_position(self) -> None:
        tree: dt.DecisionTree = read_fixture("library-loans.md")

        self.assertEqual([node.node_id for node in tree.axes()], ["A", "B", "C"])
        self.assertEqual(tree.find("B.3.1").parent_id, "B.3")
        self.assertEqual(tree.depth_of(tree.find("B.3.1")), 3)
        self.assertEqual(tree.position_id, "B")
        self.assertEqual([prerequisite.node_id for prerequisite in tree.find("B.2").prerequisites], ["C.1"])

    def test_session_log_lines_do_not_belong_to_the_last_node(self) -> None:
        tree: dt.DecisionTree = read_fixture("library-loans.md")

        body_text: str = "\n".join(text for _, text in tree.find("C.1").body)

        self.assertNotIn("다시 보지 않았다", body_text)

    def test_split_files_are_placed_under_the_decision_holding_their_link_line(self) -> None:
        tree: dt.DecisionTree = read_fixture("split/orders-decision-tree.md")

        self.assertEqual(len(tree.files), 3)
        self.assertIsNone(tree.find("B").parent_id)
        self.assertEqual(tree.find("B.2").parent_id, "B")
        self.assertEqual(tree.depth_of(tree.find("B.2.1")), 3)
        self.assertEqual(tree.find("C").prerequisites[0].node_id, "B.2")
        self.assertEqual(tree.read_findings, [])

    def test_position_prefers_a_decision_id_that_exists(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path: Path = write_tree(Path(folder), "tree.md", """
                ## 현재 상태

                - 작업 위치: R19 토론과 API 계약 논의를 마친 뒤 B.2

                ## 결정 트리

                - B [settled] 축
                  - B.2 [open] 결정
            """)
            tree: dt.DecisionTree = dt.TreeReader().read(path)

        self.assertEqual(tree.position_id, "B.2")

    def test_old_single_document_reads_without_front_matter_or_status_block(self) -> None:
        tree: dt.DecisionTree = read_fixture("old-format.md")

        self.assertEqual([node.node_id for node in tree.all_nodes()], ["A", "A.1", "B"])
        self.assertEqual(tree.position_id, "B")
        self.assertEqual(tree.find("A.1").prerequisites, [])


class MapTest(unittest.TestCase):
    def test_map_counts_statuses_and_lists_waiting_questions_and_interpretations(self) -> None:
        tree_map: dt.TreeMap = dt.build_map(read_fixture("library-loans.md"))

        self.assertEqual(tree_map.status_counts, {"open": 3, "blocked": 1, "settled": 5, "withdrawn": 0})
        self.assertEqual([node.node_id for node in tree_map.waiting_questions], ["B.3"])
        self.assertEqual([node.node_id for node, _, _ in tree_map.unconfirmed_interpretations], ["C.1"])
        axis_b: dt.AxisSummary = tree_map.axes[1]
        self.assertEqual((axis_b.decision_count, axis_b.max_depth), (5, 3))

    def test_map_spans_split_files(self) -> None:
        tree_map: dt.TreeMap = dt.build_map(read_fixture("split/orders-decision-tree.md"))

        self.assertEqual(sum(tree_map.status_counts.values()), 6)
        self.assertEqual([node.node_id for _, node in tree_map.outline], ["A", "B", "B.1", "B.2", "B.2.1", "C"])

    def test_map_json_is_valid_json(self) -> None:
        exit_code: int
        output: str
        exit_code, output, _ = run_main(["map", str(FIXTURES / "library-loans.md"), "--json"])

        payload: dict[str, object] = json.loads(output)
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["position"], "B")


class NextTest(unittest.TestCase):
    def test_unsettled_prerequisite_is_asked_before_the_decision_waiting_on_it(self) -> None:
        tree: dt.DecisionTree = read_fixture("library-loans.md")

        result: dt.NextDecision = dt.NextDecisionFinder(tree).find(tree.position_id)

        self.assertEqual(result.node.node_id, "C.1")
        self.assertIn("B.2 waits on C.1 (선행)", result.reasons)

    def test_sibling_is_asked_before_a_deeper_child(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path: Path = write_tree(Path(folder), "tree.md", """
                - A [settled] 축
                  - A.1 [settled] 앞 결정
                    - A.1.1 [open] 깊은 결정
                  - A.2 [open] 형제 결정
            """)
            result: dt.NextDecision = dt.NextDecisionFinder(dt.TreeReader().read(path)).find("A")

        self.assertEqual(result.node.node_id, "A.2")

    def test_open_axis_decision_comes_before_its_children(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path: Path = write_tree(Path(folder), "tree.md", """
                - A [open] 축의 자기 결정
                  - A.1 [open] 하위 결정
            """)
            result: dt.NextDecision = dt.NextDecisionFinder(dt.TreeReader().read(path)).find("A.1")

        self.assertEqual(result.node.node_id, "A")

    def test_search_moves_to_the_next_axis_and_wraps_around(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path: Path = write_tree(Path(folder), "tree.md", """
                - A [open] 첫 축
                - B [settled] 둘째 축
                  - B.1 [settled] 끝난 결정
                - C [settled] 셋째 축
            """)
            result: dt.NextDecision = dt.NextDecisionFinder(dt.TreeReader().read(path)).find("B")

        self.assertEqual(result.node.node_id, "A")
        self.assertIn("axis B has no decision that can be answered now", result.reasons)

    def test_withdrawn_prerequisite_leaves_nothing_to_ask(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path: Path = write_tree(Path(folder), "tree.md", """
                - A [settled] 축
                  - A.1 [withdrawn] 철회한 결정
                  - A.2 [blocked] 철회한 결정을 기다림
                    선행: A.1 철회한 결정
            """)
            result: dt.NextDecision = dt.NextDecisionFinder(dt.TreeReader().read(path)).find("A")

        self.assertIsNone(result.node)
        self.assertIn("only decisions that cannot be answered now remain: A.2", result.reasons)

    def test_blocked_decision_with_settled_prerequisites_is_returned_with_a_status_note(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path: Path = write_tree(Path(folder), "tree.md", """
                - A [settled] 축
                  - A.1 [settled] 앞 결정
                  - A.2 [blocked] 풀린 결정
                    선행: A.1 앞 결정
            """)
            result: dt.NextDecision = dt.NextDecisionFinder(dt.TreeReader().read(path)).find("A")

        self.assertEqual(result.node.node_id, "A.2")
        self.assertIn("A.2 is marked blocked but every prerequisite is settled; change it to open", result.reasons)

    def test_fully_settled_tree_has_no_next_decision(self) -> None:
        tree: dt.DecisionTree = read_fixture("old-format.md")
        tree.find("B").status_word = "settled"

        result: dt.NextDecision = dt.NextDecisionFinder(tree).find("B")

        self.assertIsNone(result.node)
        self.assertIn("every decision is settled or withdrawn", result.reasons)

    def test_from_option_overrides_the_recorded_position(self) -> None:
        exit_code: int
        output: str
        exit_code, output, _ = run_main(["next", str(FIXTURES / "split" / "orders-decision-tree.md"), "--from", "A", "--json"])

        payload: dict[str, object] = json.loads(output)
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["next"]["id"], "B.2")
        self.assertIn("current position is A, so the search starts in axis A", payload["reasons"])


class CheckTest(unittest.TestCase):
    def test_clean_trees_have_no_findings(self) -> None:
        for name in ("library-loans.md", "old-format.md", "split/orders-decision-tree.md"):
            with self.subTest(tree=name):
                self.assertEqual(dt.TreeChecker(read_fixture(name)).check(), [])

    def test_broken_tree_reports_each_kind_of_problem(self) -> None:
        findings: list[dt.Finding] = dt.TreeChecker(read_fixture("broken.md")).check()

        codes: list[str] = sorted(finding.code for finding in findings)
        self.assertEqual(codes, sorted([
            "duplicate-id",
            "unknown-status",
            "missing-prerequisite",
            "prerequisite-cycle",
            "status-mismatch", "status-mismatch", "status-mismatch",
            "prerequisite-format",
            "label-format", "label-format", "label-format",
        ]))
        label_severities: set[dt.Severity] = {finding.severity for finding in findings if finding.code == "label-format"}
        self.assertEqual(label_severities, {dt.Severity.WARNING})
        mismatched: list[str] = sorted(finding.message.split()[0] for finding in findings if finding.code == "status-mismatch")
        self.assertEqual(mismatched, ["A.1", "A.2", "A.3"])

    def test_check_exit_code_reflects_errors(self) -> None:
        broken_exit: int = run_main(["check", str(FIXTURES / "broken.md")])[0]
        clean_exit: int = run_main(["check", str(FIXTURES / "library-loans.md")])[0]

        self.assertEqual((broken_exit, clean_exit), (1, 0))

    def test_old_style_labels_are_warnings_and_keep_exit_code_zero(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path: Path = write_tree(Path(folder), "tree.md", """
                - A [settled] 옛 형식 축
                  사용자 결정: (가). 날짜 없이 적던 옛 줄
            """)
            findings: list[dt.Finding] = dt.TreeChecker(dt.TreeReader().read(path)).check()
            exit_code: int = run_main(["check", str(path)])[0]

        self.assertEqual([(finding.severity, finding.code) for finding in findings], [(dt.Severity.WARNING, "label-format")])
        self.assertEqual(exit_code, 0)

    def test_split_file_problems_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            trunk: Path = write_tree(Path(folder), "pay-decision-tree.md", """
                - A [settled] 축
            """)
            write_tree(Path(folder), "pay-decision-tree/pay-decision-tree.B.md", """
                ---
                root: C
                parent: "[[pay-decision-tree]]"
                ---

                - B [open] 링크 줄이 없는 축
            """)
            findings: list[dt.Finding] = dt.TreeChecker(dt.TreeReader().read(trunk)).check()

        messages: list[str] = [finding.message for finding in findings if finding.code == "front-matter"]
        self.assertEqual(len(messages), 3)
        self.assertTrue(any("description" in message for message in messages))
        self.assertTrue(any("root is C" in message for message in messages))
        self.assertTrue(any("no link line" in message for message in messages))


class ImpactTest(unittest.TestCase):
    def test_prerequisite_reference_is_found(self) -> None:
        tree: dt.DecisionTree = read_fixture("library-loans.md")

        impact: dt.Impact = dt.find_impact(tree, tree.find("C.1"))

        self.assertEqual([(entry.node.node_id, entry.reasons) for entry in impact.entries], [("B.2", ["prerequisite"])])

    def test_mentions_respect_id_boundaries_and_skip_the_session_log(self) -> None:
        tree: dt.DecisionTree = read_fixture("library-loans.md")

        impact: dt.Impact = dt.find_impact(tree, tree.find("A.1"))

        self.assertEqual([(entry.node.node_id, entry.reasons) for entry in impact.entries], [("C.1", ["mention"])])
        self.assertEqual(len(impact.status_block_mentions), 1)

    def test_descendants_are_listed(self) -> None:
        tree: dt.DecisionTree = read_fixture("library-loans.md")

        impact: dt.Impact = dt.find_impact(tree, tree.find("B.3"))

        self.assertEqual([(entry.node.node_id, entry.reasons) for entry in impact.entries], [("B.3.1", ["descendant"])])

    def test_unknown_decision_is_a_usage_error(self) -> None:
        exit_code: int
        error_output: str
        exit_code, _, error_output = run_main(["impact", str(FIXTURES / "library-loans.md"), "Q.7"])

        self.assertEqual(exit_code, 2)
        self.assertIn("no decision Q.7", error_output)

    def test_missing_tree_file_is_a_read_error(self) -> None:
        exit_code: int = run_main(["map", str(FIXTURES / "no-such-tree.md")])[0]

        self.assertEqual(exit_code, 2)


if __name__ == "__main__":
    unittest.main()
