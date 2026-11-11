import pytest
from dh_harness.tdd.detector import FalseTestDetector, TestDefectType

def test_detect_empty_test_body():
    code = """
def test_sample_empty():
    pass
"""
    detector = FalseTestDetector()
    defects = detector.inspect_source(code)
    assert len(defects) == 1
    assert defects[0].defect_type == TestDefectType.EMPTY_BODY
    assert defects[0].function_name == "test_sample_empty"

def test_detect_no_assertions():
    code = """
def test_no_asserts():
    a = 1 + 2
    b = a * 3
    print(b)
"""
    detector = FalseTestDetector()
    defects = detector.inspect_source(code)
    assert len(defects) == 1
    assert defects[0].defect_type == TestDefectType.NO_ASSERTION
    assert defects[0].function_name == "test_no_asserts"

def test_detect_trivial_assert_true():
    code = """
def test_trivial():
    x = 42
    assert True
"""
    detector = FalseTestDetector()
    defects = detector.inspect_source(code)
    assert len(defects) == 1
    assert defects[0].defect_type == TestDefectType.TRIVIAL_ASSERTION_CONSTANT
    assert "constant" in defects[0].description.lower() or "trivial" in defects[0].description.lower()

def test_detect_trivial_tautology():
    code = """
def test_tautology():
    assert 1 == 1
"""
    detector = FalseTestDetector()
    defects = detector.inspect_source(code)
    assert len(defects) == 1
    assert defects[0].defect_type == TestDefectType.TRIVIAL_ASSERTION_TAUTOLOGY

def test_allow_legitimate_test_with_assert():
    code = """
def test_legitimate():
    result = calculate_tax(100)
    assert result == 15
"""
    detector = FalseTestDetector()
    defects = detector.inspect_source(code)
    assert len(defects) == 0

def test_allow_pytest_raises_context_manager():
    code = """
def test_exception_raising():
    with pytest.raises(ValueError):
        raise_error()
"""
    detector = FalseTestDetector()
    defects = detector.inspect_source(code)
    assert len(defects) == 0

def test_detect_variable_tautology():
    code = """
def test_var_tautology():
    x = compute_value()
    assert x == x
"""
    detector = FalseTestDetector()
    defects = detector.inspect_source(code)
    assert len(defects) == 1
    assert defects[0].defect_type == TestDefectType.TAUTOLOGY_VARIABLE
    assert "x == x" in defects[0].description

def test_detect_unittest_variable_tautology():
    code = """
def test_unittest_tautology(self):
    val = 10
    self.assertEqual(val, val)
"""
    detector = FalseTestDetector()
    defects = detector.inspect_source(code)
    assert len(defects) == 1
    assert defects[0].defect_type == TestDefectType.TAUTOLOGY_VARIABLE

def test_detect_weak_assertion_len_non_negative():
    code = """
def test_weak_len():
    items = [1, 2, 3]
    assert len(items) >= 0
"""
    detector = FalseTestDetector()
    defects = detector.inspect_source(code)
    assert len(defects) == 1
    assert defects[0].defect_type == TestDefectType.WEAK_ASSERTION_NON_NEGATIVE_LEN

def test_detect_syntax_error_as_defect():
    broken_code = """
def test_syntax_broken(
    assert True
"""
    detector = FalseTestDetector()
    defects = detector.inspect_source(broken_code)
    assert len(defects) == 1
    assert defects[0].defect_type == TestDefectType.SYNTAX_ERROR
    assert defects[0].severity == "CRITICAL"

def test_detect_missing_production_import():
    pure_mock_test = """
import pytest

def test_something():
    assert 1 + 2 == 3
"""
    detector = FalseTestDetector()
    defects = detector.inspect_source(pure_mock_test, check_production_import=True)
    assert any(d.defect_type == TestDefectType.NO_PRODUCTION_IMPORT for d in defects)
