#!/usr/bin/env python3
import subprocess
import time
import re
import os
import platform
import csv
import argparse

# ------------------------------------------------------------------
# Parse Command-Line Arguments (Optional)
# ------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Compile and run JUnit tests on student submissions.")
    parser.add_argument("--source-file", default="Lab1.java",
                        help="Name of the Java source file to look for in subfolders.")
    parser.add_argument("--test-file", default="Lab1Test.java",
                        help="Name of the JUnit test file.")
    parser.add_argument("--junit-jar", default="junit-platform-console-standalone-1.9.3.jar",
                        help="Path/name of the JUnit Console Standalone JAR.")
    parser.add_argument("--csv-output", default="test_results.csv",
                        help="Name of the CSV file to store results.")
    parser.add_argument("--test-timeout", type=int, default=3,
                        help="Timeout (in seconds) for each individual test method.")
    parser.add_argument("--compile-timeout", type=int, default=10,
                        help="Timeout (in seconds) for Java compilation.")
    parser.add_argument("--missing-output", default="missing_source_folders.csv",
                        help="Name of the CSV file listing folders that lack the source file.")
    return parser.parse_args()

# ------------------------------------------------------------------
# Main Configuration
# ------------------------------------------------------------------
def configure():
    args = parse_args()
    config = {
        "source_file_name": args.source_file,     # e.g., "Lab1.java"
        "test_file_name":   args.test_file,       # e.g., "Lab1Test.java"
        "junit_jar":        args.junit_jar,
        "csv_output_file":  args.csv_output,
        "test_timeout":     args.test_timeout,
        "compile_timeout":  args.compile_timeout,
        "missing_output_file": args.missing_output,
        "ansi_escape":      re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]'),
        "classpath_separator": ";" if platform.system() == "Windows" else ":"
    }
    return config

# ------------------------------------------------------------------
# 1) Check JUnit
# ------------------------------------------------------------------
def check_junit(junit_jar):
    print("\n🔹 Checking for JUnit JAR file...")
    if not os.path.exists(junit_jar):
        print(f"❌ ERROR: JUnit JAR file '{junit_jar}' not found! Please download/verify it.")
        exit(1)
    print(f"✅ Found JUnit JAR: {junit_jar}")

# ------------------------------------------------------------------
# 2) Check Java Installation
# ------------------------------------------------------------------
def check_java_version():
    print("\n🔹 Checking Java Version...")
    try:
        subprocess.run(["java", "--version"], check=True, capture_output=True, text=True)
    except Exception as e:
        print(f"❌ ERROR: Java is not installed or not in PATH: {e}")
        exit(1)

# ------------------------------------------------------------------
# 3) Find *All* Subfolders
# ------------------------------------------------------------------
def find_all_subfolders():
    """
    Returns a list of *all* subfolders (recursively) under the current directory.
    """
    all_folders = []
    for root, dirs, files in os.walk("."):
        # Skip the top-level '.' if you like, or include it if you consider '.' as a "folder."
        if root == ".":
            continue
        all_folders.append(root)
    return all_folders

# ------------------------------------------------------------------
# 4) Find Subfolders that Contain the Source File
# ------------------------------------------------------------------
def find_source_folders(source_file_name):
    """
    Finds all folders containing source_file_name.
    Returns a list of folder paths.
    """
    folders_with_source = []
    for root, _, files in os.walk("."):
        if source_file_name in files:
            folders_with_source.append(root)
    return folders_with_source

# ------------------------------------------------------------------
# 5) Parse Test Methods from the Test File
# ------------------------------------------------------------------
def parse_tests_from_source(test_file_name):
    """
    Parses test_file_name for methods annotated with @Test.
    Returns a list of test method names.
    """
    print(f"\n🔹 Parsing {test_file_name} for @Test methods...")

    if not os.path.exists(test_file_name):
        print(f"❌ ERROR: {test_file_name} not found.")
        exit(1)

    with open(test_file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()

    test_methods = []
    method_signature_pattern = re.compile(r'^\s*(?:public\s+)?void\s+(\w+)\s*\(')

    i = 0
    while i < len(lines):
        if "@Test" in lines[i]:
            for j in range(i + 1, len(lines)):
                sig_match = method_signature_pattern.search(lines[j].strip())
                if sig_match:
                    test_methods.append(sig_match.group(1))
                    i = j
                    break
        i += 1

    if not test_methods:
        print(f"❌ No @Test-annotated methods found in {test_file_name}.")
        exit(1)

    print(f"✅ Found {len(test_methods)} test methods.")
    return test_methods

# ------------------------------------------------------------------
# 6) Compile and Run Tests for Each Folder that has the Source File
# ------------------------------------------------------------------
def compile_and_run_tests(folder, test_methods, config):
    """
    Compiles and runs JUnit tests for the source_file in the given folder.
    Returns a dict of test_method -> result status.
    """
    source_file_name = config["source_file_name"]
    test_file_name   = config["test_file_name"]
    junit_jar        = config["junit_jar"]
    ansi_escape      = config["ansi_escape"]
    cp_sep           = config["classpath_separator"]
    test_timeout     = config["test_timeout"]
    compile_timeout  = config["compile_timeout"]

    print(f"\n🔹 Processing: {folder}")

    bin_folder = os.path.join(folder, "bin")
    os.makedirs(bin_folder, exist_ok=True)

    # Compile command
    compile_cmd = [
        "javac",
        "-d", bin_folder,
        "-cp", f".{cp_sep}{junit_jar}",
        os.path.join(folder, source_file_name),
        test_file_name
    ]

    print(f"➡️ Compiling in {folder}...")
    try:
        compile_process = subprocess.run(
            compile_cmd, capture_output=True, text=True, timeout=compile_timeout
        )
        if compile_process.returncode != 0:
            print("❌ Compilation failed! Skipping...")
            return {test: "COMPILATION ERROR" for test in test_methods}
    except subprocess.TimeoutExpired:
        print("⏳ Compilation timed out! Skipping...")
        return {test: "TIMEOUT" for test in test_methods}

    print("✅ Compilation successful!")

    # Run each test method individually
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

            print(f"✅ {method_name} completed in {elapsed_time}s")
        except subprocess.TimeoutExpired:
            print(f"⏩ Skipping {method_name} (exceeded {test_timeout}s)")
            results[method_name] = "SKIPPED"

    return results

# ------------------------------------------------------------------
# 7) Save Test Results to CSV
# ------------------------------------------------------------------
def save_results_to_csv(results, csv_output_file):
    """
    Saves test results to a CSV file.
    Each row represents a student folder, each column a test.
    Additional columns: First Name, Last Name, Student ID, Passed, Failed, Score %.
    """
    print("\n🔹 Saving test results to CSV...")

    # Collect all unique test method names
    all_test_methods = sorted(set(test for res in results.values() for test in res.keys()))

    # Define CSV headers
    headers = ["First Name", "Last Name", "Student ID", "Passed", "Failed", "Score %"] + all_test_methods

    with open(csv_output_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        
        # Write header row
        writer.writerow(headers)

        # Write test results
        for folder_name, test_results in results.items():
            first_name, last_name, student_id = extract_student_info(folder_name)

            # Count passed and failed tests
            num_passed = sum(1 for result in test_results.values() if result == "PASSED")
            num_failed = sum(1 for result in test_results.values() if result == "FAILED")
            total_tests = len(test_results)
            score_percentage = round((num_passed / total_tests) * 100, 2) if total_tests > 0 else 0

            row = [first_name, last_name, student_id, num_passed, num_failed, score_percentage] + [
                test_results.get(test, "N/A") for test in all_test_methods
            ]
            writer.writerow(row)

    print(f"✅ Test results saved to {csv_output_file}")

# ------------------------------------------------------------------
# 8) Save Missing Folders to CSV (or Just Print)
# ------------------------------------------------------------------
def save_missing_folders_to_csv(missing_folders, missing_output_file):
    """
    Writes the missing folders (those without the source file) to a simple CSV.
    """
    if not missing_folders:
        print("\n✅ All subfolders contained the source file. Nothing to report!")
        return

    print(f"\n🔹 Saving missing folders to {missing_output_file}")
    with open(missing_output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Folder Without Source File"])  # Header
        for folder in missing_folders:
            writer.writerow([folder])
    print(f"✅ Missing folders saved to {missing_output_file}")

# ------------------------------------------------------------------
# Utility Function: Extract Student Info
# ------------------------------------------------------------------
def extract_student_info(folder_name):
    """
    Extracts first name, last name, and student ID from the folder name.
    Expected format: "FirstName LastName_StudentID_assignsubmission_file"
    Returns (first_name, last_name, student_id)
    """
    folder_name = os.path.basename(folder_name)  # Just use the folder name itself
    match = re.match(r"(.+?)_(\d+)_assignsubmission_file", folder_name)

    if match:
        name_part = match.group(1)  # e.g. "John Doe"
        student_id = match.group(2) # e.g. "1234567"

        # Split name by spaces to get first and last name
        name_parts = name_part.strip().split(" ")
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:])
        else:
            first_name = name_parts[0]
            last_name = "UNKNOWN"

        return first_name, last_name, student_id

    return "UNKNOWN", "UNKNOWN", "UNKNOWN"


# ------------------------------------------------------------------
# Main Script
# ------------------------------------------------------------------
if __name__ == "__main__":
    # 1) Load configuration from CLI or defaults
    config = configure()

    # 2) Check JUnit and Java
    check_junit(config["junit_jar"])
    check_java_version()

    # 3) Identify which folders *could* have the source, and which ones actually do
    all_subfolders = find_all_subfolders()
    folders_with_source = find_source_folders(config["source_file_name"])

    # 4) Determine missing folders
    missing_folders = sorted(set(all_subfolders) - set(folders_with_source))

    if not folders_with_source:
        print(f"❌ No '{config['source_file_name']}' files found in any subdirectory.")
        if missing_folders:
            # Optionally record the missing folders
            save_missing_folders_to_csv(missing_folders, config["missing_output_file"])
        exit(1)

    # 5) Parse test methods from the test file
    test_methods = parse_tests_from_source(config["test_file_name"])

    # 6) Compile & run tests, collecting results only for folders *with* the source
    all_results = {}
    for folder in folders_with_source:
        test_results = compile_and_run_tests(folder, test_methods, config)
        all_results[folder] = test_results

    # 7) Save normal test results to CSV
    save_results_to_csv(all_results, config["csv_output_file"])

    # 8) Save the list of "missing" folders (i.e. no source file) to a separate CSV
    save_missing_folders_to_csv(missing_folders, config["missing_output_file"])

