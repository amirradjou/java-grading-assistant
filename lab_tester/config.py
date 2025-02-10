# lab_tester/config.py

import argparse
import platform
import re

def parse_args():
    parser = argparse.ArgumentParser(description="Compile and run JUnit tests on student submissions.")
    parser.add_argument("--source-file", default="Lab1.java",
                        help="Name of the Java source file to look for in subfolders.")
    parser.add_argument("--test-file", default="Lab1Test.java",
                        help="Name of the JUnit test file.")
    parser.add_argument("--junit-jar", default="junit-platform-console-standalone-1.9.3.jar",
                        help="Path/name of the JUnit Console Standalone JAR.")
    parser.add_argument("--junit-version", type=int, choices=[4, 5], default=5,
                        help="Specify the JUnit version (4 or 5). Default is JUnit 5.")
    parser.add_argument("--csv-output", default="test_results.csv",
                        help="Name of the CSV file to store results.")
    parser.add_argument("--test-timeout", type=int, default=3,
                        help="Timeout (in seconds) for each individual test method.")
    parser.add_argument("--compile-timeout", type=int, default=10,
                        help="Timeout (in seconds) for Java compilation.")
    parser.add_argument("--missing-output", default="missing_source_folders.csv",
                        help="Name of the CSV file listing folders that lack the source file.")
    return parser.parse_args()

def create_config(args):
    """
    Given the parsed arguments, return a dictionary containing
    all configuration details the rest of the script requires.
    """
    return {
        "source_file_name": args.source_file,
        "test_file_name": args.test_file,
        "junit_jar": args.junit_jar,
        "junit_version": args.junit_version,
        "csv_output_file": args.csv_output,
        "test_timeout": args.test_timeout,
        "compile_timeout": args.compile_timeout,
        "missing_output_file": args.missing_output,
        "ansi_escape": re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]'),
        "classpath_separator": ";" if platform.system() == "Windows" else ":"
    }
