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
