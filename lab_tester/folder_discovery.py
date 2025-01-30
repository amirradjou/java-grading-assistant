# lab_tester/folder_discovery.py

import os

def find_all_subfolders():
    """
    Returns a list of subfolders only at the first level under the current directory.
    Skips the top-level '.' folder for cleanliness.
    """
    all_folders = []
    for entry in os.scandir("."):
        if entry.is_dir():
            all_folders.append(entry.path)
    return all_folders

def find_source_folders(source_file_name):
    """
    Returns a list of folder paths that contain source_file_name, only checking the first-level subdirectories.
    """
    folders_with_source = []
    for entry in os.scandir("."):
        if entry.is_dir():
            for sub_entry in os.scandir(entry.path):
                if sub_entry.is_file() and sub_entry.name == source_file_name:
                    folders_with_source.append(entry.path)
                    break  # No need to check further inside this folder
    return folders_with_source

