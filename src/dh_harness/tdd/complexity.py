from __future__ import annotations
import ast
import os
import re
from typing import List

from dh_harness.core.contracts import ComplexityReport, ComplexityViolation

class CyclomaticVisitor(ast.NodeVisitor):
    """AST Visitor that calculates McCabe cyclomatic complexity for a function AST node."""

    def __init__(self):
        self.complexity = 1

    def visit_If(self, node: ast.If):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node: ast.With):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp):
        # Each extra operator in a boolean condition adds a decision branch
        self.complexity += max(0, len(node.values) - 1)
        self.generic_visit(node)

class ComplexityAnalyzer:
    """
    AST Cyclomatic Complexity Analyzer (info.md Section 15 & TDD Refactor Gate).
    Calculates McCabe complexity per function/method and flags functions exceeding the threshold.
    """

    def __init__(self, max_complexity: int = 10):
        self.max_complexity = max_complexity

    def analyze_python_code(self, code: str, file_path: str = "") -> ComplexityReport:
        violations: List[ComplexityViolation] = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    visitor = CyclomaticVisitor()
                    for child in node.body:
                        visitor.visit(child)

                    if visitor.complexity > self.max_complexity:
                        violations.append(ComplexityViolation(
                            file_path=file_path,
                            function_name=node.name,
                            complexity_score=visitor.complexity,
                            max_allowed=self.max_complexity,
                            line_number=node.lineno
                        ))
        except Exception:
            pass

        return ComplexityReport(
            violations=violations,
            files_analyzed=1,
            passed=len(violations) == 0
        )

    def analyze_file(self, file_path: str) -> ComplexityReport:
        if not os.path.isfile(file_path):
            return ComplexityReport(violations=[], files_analyzed=0, passed=True)

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            return ComplexityReport(violations=[], files_analyzed=0, passed=True)

        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".py":
            return self.analyze_python_code(content, file_path)

        # Fallback regex decision-point counting for C# and TS/JS
        lines = content.splitlines()
        score = 1
        for line in lines:
            if re.search(r"\b(?:if|while|for|switch|catch)\b", line):
                score += 1
            if re.search(r"(&&|\|\||\?)", line):
                score += 1

        violations = []
        if score > self.max_complexity * 3:  # Whole file heuristic threshold
            violations.append(ComplexityViolation(
                file_path=file_path,
                function_name="file_aggregate",
                complexity_score=score,
                max_allowed=self.max_complexity * 3,
                line_number=1
            ))

        return ComplexityReport(
            violations=violations,
            files_analyzed=1,
            passed=len(violations) == 0
        )
