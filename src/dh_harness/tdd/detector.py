from __future__ import annotations
import ast
import os
from enum import Enum
from typing import List, Dict, Optional
from pydantic import BaseModel

class TestDefectType(str, Enum):
    __test__ = False
    EMPTY_BODY = "EMPTY_BODY"
    NO_ASSERTION = "NO_ASSERTION"
    TRIVIAL_ASSERTION_CONSTANT = "TRIVIAL_ASSERTION_CONSTANT"
    TRIVIAL_ASSERTION_TAUTOLOGY = "TRIVIAL_ASSERTION_TAUTOLOGY"

class TestDefect(BaseModel):
    file_path: str = ""
    function_name: str
    line_number: int
    defect_type: TestDefectType
    description: str
    severity: str = "CRITICAL"

class FalseTestDetector:
    """
    Static analyzer based on Python AST to detect cosmetic or false tests.
    Complies with Section 7.4 of info.md:
    Detects empty tests, trivial assertions, tests with no asserts, and tautologies.
    """

    def inspect_file(self, file_path: str) -> List[TestDefect]:
        """Inspects a Python test file on disk."""
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                source = f.read()
            return self.inspect_source(source, file_path=file_path)
        except Exception as e:
            return [TestDefect(
                file_path=file_path,
                function_name="<file_parse_error>",
                line_number=1,
                defect_type=TestDefectType.NO_ASSERTION,
                description=f"Could not parse file: {e}",
                severity="CRITICAL"
            )]

    def inspect_directory(self, dir_path: str) -> Dict[str, List[TestDefect]]:
        """Recursively inspects test files in a directory."""
        results = {}
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.startswith("test_") and file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    defects = self.inspect_file(full_path)
                    if defects:
                        results[full_path] = defects
        return results

    def inspect_source(self, source_code: str, file_path: str = "") -> List[TestDefect]:
        """Inspects Python source code and returns list of defects found."""
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return []

        defects: List[TestDefect] = []

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("test_") or node.name.endswith("_test"):
                    self._inspect_function(node, file_path, defects)

        return defects

    def _inspect_function(self, func_node: ast.FunctionDef | ast.AsyncFunctionDef, file_path: str, defects: List[TestDefect]):
        # 1. Check for empty body
        body_statements = [
            stmt for stmt in func_node.body
            if not (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str))
        ]

        if not body_statements or (len(body_statements) == 1 and isinstance(body_statements[0], ast.Pass)):
            defects.append(TestDefect(
                file_path=file_path,
                function_name=func_node.name,
                line_number=func_node.lineno,
                defect_type=TestDefectType.EMPTY_BODY,
                description=f"Test function '{func_node.name}' has an empty body with no executable test logic.",
                severity="CRITICAL"
            ))
            return

        has_assert_or_raises = False

        for subnode in ast.walk(func_node):
            # Check for pytest.raises
            if isinstance(subnode, ast.With):
                for item in subnode.items:
                    if isinstance(item.context_expr, ast.Call):
                        func = item.context_expr.func
                        if (isinstance(func, ast.Attribute) and func.attr == "raises") or (isinstance(func, ast.Name) and func.id == "raises"):
                            has_assert_or_raises = True

            # Check for unittest self.assert*
            if isinstance(subnode, ast.Call):
                func = subnode.func
                if isinstance(func, ast.Attribute) and func.attr.startswith("assert"):
                    has_assert_or_raises = True

            # Check for Python assert
            if isinstance(subnode, ast.Assert):
                has_assert_or_raises = True
                test_expr = subnode.test

                # Check for constant assert (assert True, assert 1, etc.)
                if isinstance(test_expr, ast.Constant):
                    defects.append(TestDefect(
                        file_path=file_path,
                        function_name=func_node.name,
                        line_number=subnode.lineno,
                        defect_type=TestDefectType.TRIVIAL_ASSERTION_CONSTANT,
                        description=f"Trivial constant assertion 'assert {test_expr.value}' provides zero regression coverage.",
                        severity="CRITICAL"
                    ))

                # Check for tautology assert (assert 1 == 1, assert "a" == "a")
                elif isinstance(test_expr, ast.Compare):
                    left = test_expr.left
                    if test_expr.comparators and len(test_expr.comparators) == 1:
                        right = test_expr.comparators[0]
                        if isinstance(left, ast.Constant) and isinstance(right, ast.Constant):
                            if left.value == right.value:
                                defects.append(TestDefect(
                                    file_path=file_path,
                                    function_name=func_node.name,
                                    line_number=subnode.lineno,
                                    defect_type=TestDefectType.TRIVIAL_ASSERTION_TAUTOLOGY,
                                    description=f"Trivial tautological assertion '{left.value} == {right.value}' is always true.",
                                    severity="CRITICAL"
                                ))

        if not has_assert_or_raises:
            defects.append(TestDefect(
                file_path=file_path,
                function_name=func_node.name,
                line_number=func_node.lineno,
                defect_type=TestDefectType.NO_ASSERTION,
                description=f"Test function '{func_node.name}' contains no assert statements or pytest.raises expectations.",
                severity="CRITICAL"
            ))
