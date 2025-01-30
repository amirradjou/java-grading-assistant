# lab_tester/environment.py

import os
import subprocess

def check_junit(junit_jar):
    """Check if the JUnit jar file exists; raise an Exception if not."""
    if not os.path.exists(junit_jar):
        raise FileNotFoundError(f"JUnit JAR file '{junit_jar}' not found!")

def check_java_version():
    """Check if Java is installed by running 'java --version'."""
    try:
        subprocess.run(["java", "--version"], check=True, capture_output=True, text=True)
    except Exception as e:
        raise EnvironmentError(f"Java not installed or not in PATH: {e}")

def setup_environment(config):
    """
    Ensures JUnit JAR exists and Java is properly installed.
    Raises exceptions if checks fail.
    """
    print("\n🔹 Checking environment...")
    check_junit(config["junit_jar"])
    check_java_version()
    print("✅ Environment is valid.")

