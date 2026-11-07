#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deterministic Verifiers Library for Graviton TDD (AEE/ATFE).
Provides strict programmatic verifications for task steps.
"""
import os
import sys
import json
import subprocess
import shutil

def check_file_exists(file_path):
    """Checks if a file exists on the filesystem."""
    exists = os.path.exists(file_path)
    print(f"[*] Verifier: Checking if {file_path} exists -> {exists}")
    return exists

def check_file_size(file_path, min_bytes=10):
    """Checks if a file exists and has size >= min_bytes."""
    if not os.path.exists(file_path):
        print(f"[-] Verifier: File {file_path} does not exist.")
        return False
    size = os.path.getsize(file_path)
    ok = size >= min_bytes
    print(f"[*] Verifier: Checking size of {file_path} ({size} bytes) >= {min_bytes} -> {ok}")
    return ok

def check_file_contains(file_path, expected_text):
    """Checks if a file exists and contains expected text."""
    if not os.path.exists(file_path):
        print(f"[-] Verifier: File {file_path} does not exist.")
        return False
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        found = expected_text in content
        print(f"[*] Verifier: Checking if {file_path} contains '{expected_text}' -> {found}")
        return found
    except Exception as e:
        print(f"[-] Verifier Error: Could not read {file_path}: {e}")
        return False

def get_python_executable():
    """Returns .venv python executable if present, otherwise sys.executable."""
    is_win = sys.platform == "win32"
    venv_py = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe") if is_win else os.path.join(os.getcwd(), ".venv", "bin", "python")
    if os.path.exists(venv_py):
        return venv_py
    return sys.executable

def check_python_test(test_script_path, cwd=None):
    """Runs a Python script and verifies if it exits with code 0."""
    if not os.path.exists(test_script_path):
        print(f"[-] Verifier: Test script {test_script_path} not found.")
        return False
    print(f"[*] Verifier: Running test script {test_script_path}...")
    py_bin = get_python_executable()
    try:
        res = subprocess.run([py_bin, test_script_path], capture_output=True, text=True, cwd=cwd, timeout=60)
        ok = res.returncode == 0
        print(f"[*] Verifier: Exit code {res.returncode}. Output:\n{res.stdout}\nErrors:\n{res.stderr}")
        return ok
    except Exception as e:
        print(f"[-] Verifier Error: Exception running test: {e}")
        return False

def check_python_syntax(file_path):
    """Parses a Python file using AST to ensure there are no syntax errors."""
    if not os.path.exists(file_path):
        print(f"[-] Verifier: Python file {file_path} not found.")
        return False
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        import ast
        ast.parse(source)
        print(f"[*] Verifier: AST syntax check for {file_path} PASSED.")
        return True
    except SyntaxError as e:
        print(f"[-] Verifier: Syntax error in {file_path}:\n    Line {e.lineno}: {e.msg}\n    Code: {e.text.strip() if e.text else ''}")
        return False
    except Exception as e:
        print(f"[-] Verifier: Error parsing syntax for {file_path}: {e}")
        return False

def check_sdk_installed(package_name="google.antigravity"):
    """Checks if a Python module/package can be imported successfully."""
    print(f"[*] Verifier: Checking import for '{package_name}'...")
    try:
        __import__(package_name)
        print(f"[+] Verifier: Package '{package_name}' is installed and importable.")
        return True
    except ImportError as e:
        print(f"[-] Verifier: Failed to import '{package_name}': {e}")
        return False

def check_npm_binary(bin_path):
    """Verifies that the Node CLI wrapper file exists and has executable syntax."""
    if not os.path.exists(bin_path):
        print(f"[-] Verifier: CLI binary {bin_path} does not exist.")
        return False
    try:
        res = subprocess.run(["node", "-c", bin_path], capture_output=True, text=True)
        ok = res.returncode == 0
        print(f"[*] Verifier: Syntax check on {bin_path} -> {'OK' if ok else 'FAIL'}")
        return ok
    except Exception as e:
        print(f"[-] Verifier: Node syntax check failed: {e}")
        return False

def check_pytest_suite(test_dir="tests"):
    """Runs pytest on test_dir and verifies all tests pass."""
    print(f"[*] Verifier: Running pytest on {test_dir}...")
    py_bin = get_python_executable()
    try:
        res = subprocess.run([py_bin, "-m", "pytest", test_dir], capture_output=True, text=True)
        ok = res.returncode == 0
        print(f"[*] Verifier: pytest exit code {res.returncode}.\nOutput:\n{res.stdout}\nStderr:\n{res.stderr}")
        return ok
    except Exception as e:
        print(f"[-] Verifier: pytest execution error: {e}")
        return False

def check_image_corrupted(image_path):
    """Verifies image integrity if PIL is available."""
    if not os.path.exists(image_path):
        return False
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def check_layout_overlaps(bbox_json_path):
    """Stub for layout bounding box overlaps check."""
    return os.path.exists(bbox_json_path)

if __name__ == "__main__":
    print("[*] Graviton Verifiers library loaded successfully.")
