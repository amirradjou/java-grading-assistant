# lab_tester/student_info.py

import os
import re

def extract_student_info(folder_name):
    """
    Extracts first name, last name, and student ID from the folder name.
    Expected format: "FirstName LastName_StudentID_assignsubmission_file"
    Returns (first_name, last_name, student_id)
    """
    folder_basename = os.path.basename(folder_name)
    match = re.match(r"(.+?)_(\d+)_assignsubmission_file", folder_basename)

    if match:
        name_part = match.group(1)  # e.g. "John Doe"
        student_id = match.group(2) # e.g. "1234567"

        name_parts = name_part.strip().split(" ")
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:])
        else:
            first_name = name_parts[0]
            last_name = "UNKNOWN"

        return first_name, last_name, student_id

    return "UNKNOWN", "UNKNOWN", "UNKNOWN"

