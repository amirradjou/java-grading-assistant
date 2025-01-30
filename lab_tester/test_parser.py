# lab_tester/test_parser.py

import os
import re

def parse_tests_from_source(test_file_name):
    """
    Parses `test_file_name` for methods annotated with @Test.
    Returns a list of test method names.
    """
    print(f"\n🔹 Parsing {test_file_name} for @Test methods...")

    if not os.path.exists(test_file_name):
        raise FileNotFoundError(f"{test_file_name} not found.")

    with open(test_file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()

    test_methods = []
    method_signature_pattern = re.compile(r'^\s*(?:public\s+)?void\s+(\w+)\s*\(')

    i = 0
    while i < len(lines):
        if "@Test" in lines[i]:
            # Search the subsequent lines for a method signature
            for j in range(i + 1, len(lines)):
                sig_match = method_signature_pattern.search(lines[j].strip())
                if sig_match:
                    test_methods.append(sig_match.group(1))
                    i = j
                    break
        i += 1

    if not test_methods:
        raise ValueError(f"No @Test-annotated methods found in {test_file_name}.")

    print(f"✅ Found {len(test_methods)} test methods: {', '.join(test_methods)}")
    return test_methods

