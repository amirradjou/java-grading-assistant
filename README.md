Project Structure
-----------------

```
lab_tester/
    ├── __init__.py
    ├── config.py
    ├── environment.py
    ├── folder_discovery.py
    ├── test_parser.py
    ├── compiler.py
    ├── runner.py
    ├── csv_utils.py
    ├── student_info.py
─ main.py
```

-   **`config.py`**: Handles parsing of command-line arguments and building a configuration dictionary.
-   **`environment.py`**: Checks the environment (e.g., JUnit JAR file, Java installation).
-   **`folder_discovery.py`**: Scans subfolders for the specified source file.
-   **`test_parser.py`**: Parses the JUnit test file to discover `@Test`-annotated methods.
-   **`compiler.py`**: Compiles the student Java source and the test file.
-   **`runner.py`**: Runs each discovered test method individually.
-   **`csv_utils.py`**: Saves results and missing-folders lists to CSV.
-   **`student_info.py`**: Extracts student information (First/Last Name, ID) from folder names.
-   **`main.py`**: The main entry point that orchestrates the entire process.

* * * * *

Prerequisites
-------------

1.  **Python 3.7+**\
    Make sure Python 3 is installed and available on your system.
2.  **Java 11+**\
    The script expects `java` to be available in your system's PATH.
3.  **JUnit Console Standalone JAR**\
    By default, we look for `junit-platform-console-standalone-1.9.3.jar` in the current directory.
* * * * *

Installation
------------

1.  **Clone or Download** this repository from GitHub:

    ```
    git clone https://github.com/amirradjou/java-grading-assistant.git
    cd java-grading-assistant
    ```


* * * * *

Usage
-----

### Basic Command

From the `java-grading-assistant/` directory, run:


`python main.py [OPTIONS...]`

The script will:

1.  Check if the JUnit JAR exists.
2.  Check your Java installation by running `java --version`.
3.  Recursively scan all subfolders for the required source file (default is `Lab1.java`).
4.  Parse your test file (default is `Lab1Test.java`) for `@Test` methods.
5.  For each folder that has the source file, compile and run the tests.
6.  Write results to a CSV file (default `test_results.csv`).
7.  Write a list of folders missing the source file to another CSV (default `missing_source_folders.csv`).

### Command-Line Options

| Option | Description | Default |
| --- | --- | --- |
| `--source-file` | Name of the Java source file to look for in subfolders. | `Lab1.java` |
| `--test-file` | Name of the JUnit test file. | `Lab1Test.java` |
| `--junit-jar` | Path/name of the JUnit Console Standalone JAR. | `junit-platform-console-standalone-1.9.3.jar` |
| `--csv-output` | Name of the CSV file to store results. | `test_results.csv` |
| `--test-timeout` | Timeout (in seconds) for each test method. | `3` |
| `--compile-timeout` | Timeout (in seconds) for Java compilation. | `10` |
| `--missing-output` | Name of the CSV file listing folders that lack the source file. | `missing_source_folders.csv` |

For example:


`python main.py\
  --source-file Lab2.java\
  --test-file Lab2Test.java\
  --junit-jar path/to/junit-platform-console-standalone-1.9.3.jar\
  --csv-output lab2_results.csv\
  --missing-output lab2_missing.csv\
  --test-timeout 5\
  --compile-timeout 15`

* * * * *

Output Files
------------

1.  **Test Results CSV** (default: `test_results.csv`)

    Each row represents a single folder (student submission). The columns include:

    -   First Name
    -   Last Name
    -   Student ID
    -   Passed (number of test methods that passed)
    -   Failed (number of test methods that failed)
    -   Score % (percentage of passed tests)
    -   One column for each test method's result (e.g., "PASSED", "FAILED", "COMPILATION ERROR", etc.)
2.  **Missing Folders CSV** (default: `missing_source_folders.csv`)

    Contains a list of folders that *did not* contain the required source file. One folder path per line.

* * * * *

Troubleshooting & Tips
----------------------

1.  **JUnit JAR Not Found**
    -   Make sure `junit-platform-console-standalone-x.x.x.jar` is in the same directory or specify its location with `--junit-jar`.
2.  **Java Not Found**
    -   Ensure `java` is on your `PATH`. On Linux/macOS, you can check with `which java`. On Windows, check your system environment variables.
3.  **Compilation Errors**
    -   If compilation fails for a folder, that submission's test methods are marked as "COMPILATION ERROR" in the results CSV.
    -   Check the "stderr" messages printed in the console for details.
4.  **Timeout Issues**
    -   Increase `--test-timeout` or `--compile-timeout` if your Java code requires longer. The defaults are fairly short.
5.  **Folder Name Parsing**
    -   By default, the script expects a folder name like `John Doe_123456_assignsubmission_file` to extract "John", "Doe", and "123456" as student details. Adapt the regex in `student_info.py` if your naming convention differs.


* * * * *

