Java Grading Assistant Script
========================================

This script automates the process of compiling and running JUnit tests for student submissions in an Object-Oriented Programming (OOP) course. It scans student folders, compiles their Java code, runs predefined JUnit tests, and records the results in a CSV file.

Features
--------

-   **Automated Compilation & Testing**: Compiles Java submissions and runs JUnit tests for each student.

-   **JUnit Support**: Uses `junit-platform-console-standalone-1.9.3.jar` for testing.

-   **Timeout Handling**: Stops tests if they exceed a set duration.

-   **CSV Report Generation**: Outputs detailed test results including student performance.

-   **Error Handling**: Reports missing source files and compilation failures.

Prerequisites
-------------

Before running the script, ensure you have:

-   **Java Development Kit (JDK)** installed and added to the system `PATH`.

-   **JUnit Platform Console Standalone JAR** (`junit-platform-console-standalone-1.9.3.jar`) downloaded.

-   **Python 3** installed to run the script.

Installation & Setup
--------------------

1.  **Clone the Repository:**

    ```
    git clone https://github.com/amirradjou/java-grading-assistant.git
    cd java-grading-assistant
    ```

2.  **Place JUnit JAR in the directory:** Ensure `junit-platform-console-standalone-1.9.3.jar` is in the same folder as the script.

3.  **Prepare Test File:**

    -   Place the test file (e.g., `Lab1Test.java`) in the root directory.

    -   Ensure the test file contains JUnit test cases for grading.
  
    -   Ensure the Submission directories are present in the root directory.

Usage
-----

Run the script from the command line:

```
python3 main.py
```

By default, the script looks for `Lab1.java` in student folders and `Lab1Test.java` as the test file.

### Command-Line Arguments

You can customize the script using the following arguments:

```
python3 main.py\
    --source-file Lab1.java\
    --test-file Lab1Test.java\
    --junit-jar junit-platform-console-standalone-1.9.3.jar\
    --csv-output test_results.csv\
    --test-timeout 3\
    --compile-timeout 10\
    --missing-output missing_source_folders.csv
```
```
| Argument | Description | Default |
| `--source-file` | Name of the student Java file | `Lab1.java` |
| `--test-file` | Name of the JUnit test file | `Lab1Test.java` |
| `--junit-jar` | Path to the JUnit JAR file | `junit-platform-console-standalone-1.9.3.jar` |
| `--csv-output` | Output CSV file for results | `test_results.csv` |
| `--test-timeout` | Timeout per test (seconds) | `3` |
| `--compile-timeout` | Timeout for compilation (seconds) | `10` |
| `--missing-output` | CSV file for folders missing source files | `missing_source_folders.csv` |
```

Output
------

1.  **Test Results CSV (**`**test_results.csv**`**)**:

    -   Contains student test results with the number of passed/failed tests and scores.

2.  **Missing Source Folders CSV (**`**missing_source_folders.csv**`**)**:

    -   Lists student folders where the required Java source file was not found.

Troubleshooting
---------------

-   **JUnit JAR Not Found?**

    -   Ensure `junit-platform-console-standalone-1.9.3.jar` is in the script directory.

-   **Java Not Recognized?**

    -   Check if Java is installed and available in the system `PATH` by running:

        ```
        java --version
        ```
