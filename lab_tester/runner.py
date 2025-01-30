# lab_tester/runner.py

import os
import subprocess
import time

def run_tests(folder, test_methods, config):
    """
    Runs each test method individually in the specified `folder`.
    Returns a dict mapping {test_method_name: "PASSED"/"FAILED"/"UNKNOWN"/"SKIPPED"}.
    """
    junit_jar       = config["junit_jar"]
    ansi_escape     = config["ansi_escape"]
    cp_sep          = config["classpath_separator"]
    test_timeout    = config["test_timeout"]

    bin_folder = os.path.join(folder, "bin")
    results = {}

    for method_name in test_methods:
        test_run_cmd = [
            "java", "-jar", junit_jar,
            "--class-path", bin_folder,
            "--select-method", f"Lab1Test#{method_name}"
        ]
        print(f"▶️ Running test: {method_name} in {folder}")

        try:
            start_time = time.time()
            test_process = subprocess.run(
                test_run_cmd, capture_output=True, text=True, timeout=test_timeout
            )
            elapsed_time = round(time.time() - start_time, 2)

            # Remove ANSI codes
            test_output = ansi_escape.sub('', test_process.stdout + "\n" + test_process.stderr)
            test_output_lower = test_output.lower()

            if "tests successful" in test_output_lower:
                results[method_name] = "PASSED"
            elif "tests failed" in test_output_lower:
                results[method_name] = "FAILED"
            else:
                results[method_name] = "UNKNOWN"

            print(f"   → {method_name} completed in {elapsed_time}s: {results[method_name]}")
        except subprocess.TimeoutExpired:
            print(f"   → Skipping {method_name} (exceeded {test_timeout}s)")
            results[method_name] = "SKIPPED"

    return results

