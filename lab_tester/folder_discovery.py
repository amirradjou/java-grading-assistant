# lab_tester/folder_discovery.py

import os

def find_all_subfolders():
    """
    Returns a list of *all* subfolders (recursively) under the current directory.
    Skips the top-level '.' folder for cleanliness.
    """
    all_folders = []
    for root, dirs, files in os.walk("."):
        if root == ".":
            continue
        all_folders.append(root)
    return all_folders

def find_source_folders(source_file_name):
    """
    Returns a list of folder paths that contain `source_file_name`.
    """
    folders_with_source = []
    for root, _, files in os.walk("."):
        if source_file_name in files:
            folders_with_source.append(root)
    return folders_with_source

