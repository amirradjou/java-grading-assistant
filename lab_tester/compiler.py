# lab_tester/compiler.py

import os
import subprocess

def compile_sources(folder, config):
    """
    Compiles the source file and the test file into `folder/bin`.
    Returns True if compilation succeeds, False otherwise.
    """
    source_file_name = config["source_file_name"]
    test_file_name   = config["test_file_name"]
    junit_jar        = config["junit_jar"]
    cp_sep           = config["classpath_separator"]
    compile_timeout  = config["compile_timeout"]

    bin_folder = os.path.join(folder, "bin")
    os.makedirs(bin_folder, exist_ok=True)

    compile_cmd = [
        "javac",
        "-d", bin_folder,
        "-cp", f".{cp_sep}{junit_jar}",
        os.path.join(folder, source_file_name),
        test_file_name
    ]

    print(f"➡️ Compiling in: {folder}")
    try:
        compile_process = subprocess.run(
            compile_cmd, capture_output=True, text=True, timeout=compile_timeout
        )
        if compile_process.returncode != 0:
            print("❌ Compilation failed!")
            print(compile_process.stderr.strip())
            return False
        print("✅ Compilation successful!")
        return True
    except subprocess.TimeoutExpired:
        print("⏳ Compilation timed out!")
        return False

