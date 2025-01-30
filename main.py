# lab_tester/main.py

import sys

from lab_tester.config import parse_args, create_config
from lab_tester.environment import setup_environment
from lab_tester.folder_discovery import find_all_subfolders, find_source_folders
from lab_tester.test_parser import parse_tests_from_source
from lab_tester.compiler import compile_sources
from lab_tester.runner import run_tests
from lab_tester.csv_utils import save_results_to_csv, save_missing_folders_to_csv


def main():
    # 1) Parse CLI arguments and create the config
    args = parse_args()
    config = create_config(args)

    # 2) Check environment (Java, JUnit, etc.)
    try:
        setup_environment(config)
    except Exception as e:
        print(f"❌ Environment error: {e}")
        sys.exit(1)

    # 3) Gather folder info
    all_subfolders = find_all_subfolders()
    folders_with_source = find_source_folders(config["source_file_name"])
    missing_folders = sorted(set(all_subfolders) - set(folders_with_source))

    if not folders_with_source:
        print(f"❌ No '{config['source_file_name']}' files found.")
        if missing_folders:
            save_missing_folders_to_csv(missing_folders, config["missing_output_file"])
        sys.exit(1)

    # 4) Parse test methods
    try:
        test_methods = parse_tests_from_source(config["test_file_name"])
    except Exception as e:
        print(f"❌ Test file error: {e}")
        sys.exit(1)

    # 5) Compile & run tests
    all_results = {}
    for folder in folders_with_source:
        print(f"\n🔹 Processing folder: {folder}")
        compiled_ok = compile_sources(folder, config)
        if compiled_ok:
            test_results = run_tests(folder, test_methods, config)
        else:
            # If compilation fails, mark all test methods accordingly
            test_results = {method: "COMPILATION ERROR" for method in test_methods}
        all_results[folder] = test_results

    # 6) Save results to CSV
    save_results_to_csv(all_results, config["csv_output_file"])

    # 7) Save missing folders
    save_missing_folders_to_csv(missing_folders, config["missing_output_file"])

    print("\n✅ All done!")


if __name__ == "__main__":
    main()

