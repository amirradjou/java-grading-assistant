import os
import subprocess
import time

def run_tests(folder, test_methods, config):
    """
    Runs each test method individually in the specified `folder`, supporting both JUnit 4 and JUnit 5.
    Returns a dict mapping {test_method_name: "PASSED"/"FAILED"/"UNKNOWN"/"SKIPPED"}.
    """
    junit_jar       = config["junit_jar"]
    junit_version   = config.get("junit_version", 5)
    ansi_escape     = config["ansi_escape"]
    cp_sep          = config["classpath_separator"]
    test_timeout    = config["test_timeout"]
    test_file_name  = config["test_file_name"].split(".")[0]

    bin_folder = os.path.join(folder, "bin")
    results = {}

    # Construct classpath (JUnit JAR + compiled class files)
    classpath = f"{bin_folder}{cp_sep}{junit_jar}"

    for method_name in test_methods:
        if junit_version == 4:
            # JUnit 4 execution: run the entire test class
            test_run_cmd = [
                "java", "-cp", classpath,
                "org.junit.runner.JUnitCore", f"lab1.{test_file_name}"
            ]
        else:
            # JUnit 5 execution: run individual methods
            test_run_cmd = [
                "java", "-jar", junit_jar,
                "--class-path", f"{bin_folder}{cp_sep}.",
                "--select-method", f"{test_file_name}#{method_name}"
            ]

        print(f"▶️ Running test: {method_name} in {folder} (JUnit {junit_version})")

        try:
            start_time = time.time()
            test_process = subprocess.run(
                test_run_cmd, capture_output=True, text=True, timeout=test_timeout
            )
            elapsed_time = round(time.time() - start_time, 2)

            # Remove ANSI codes
            test_output = ansi_escape.sub('', test_process.stdout + "\n" + test_process.stderr)
            test_output_lower = test_output.lower()

            # Parse test results based on JUnit version
            if junit_version == 4:
                if "ok" in test_output_lower:
                    results[method_name] = "PASSED"
                elif "failures" in test_output_lower or "failure" in test_output_lower:
                    results[method_name] = "FAILED"
                else:
                    results[method_name] = "UNKNOWN"
            else:
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

