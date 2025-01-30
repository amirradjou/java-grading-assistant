# lab_tester/csv_utils.py

import csv

from lab_tester.student_info import extract_student_info

def save_results_to_csv(results, csv_output_file):
    """
    Saves test results to a CSV file.
    Each row represents a student folder, each column a test.
    Additional columns: First Name, Last Name, Student ID, Passed, Failed, Score %.
    """
    print(f"\n🔹 Saving test results to {csv_output_file}...")

    # Collect all unique test method names
    all_test_methods = sorted(set(
        method for folder_dict in results.values() for method in folder_dict.keys()
    ))

    headers = ["First Name", "Last Name", "Student ID",
               "Passed", "Failed", "Score %"] + all_test_methods

    with open(csv_output_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for folder_name, test_dict in results.items():
            first_name, last_name, student_id = extract_student_info(folder_name)

            num_passed = sum(1 for res in test_dict.values() if res == "PASSED")
            num_failed = sum(1 for res in test_dict.values() if res == "FAILED" or res == "COMPILATION ERROR" or res == "SKIPPED")
            total_tests = len(test_dict)
            score_percentage = round(
                (num_passed / total_tests) * 100, 2
            ) if total_tests else 0

            row = [
                first_name,
                last_name,
                student_id,
                num_passed,
                num_failed,
                score_percentage
            ] + [test_dict.get(m, "N/A") for m in all_test_methods]

            writer.writerow(row)

    print(f"✅ Results written to {csv_output_file}")

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

