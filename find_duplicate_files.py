#!/usr/bin/env python3

from os.path import join, exists, isfile, islink, getsize, abspath
from argparse import ArgumentParser
from os import access, R_OK
from hashlib import md5
from json import dumps
from os import walk


# ---------------------Get Argument From User----------------------
def get_argument():
    """
    Return an absolute path which is inputted
    by the user through the command line.

    @return: an absolute path of a directory.
    """
    parser = ArgumentParser(prog="Duplicate Files Finder")
    parser.add_argument('-p', '--path', type=str,
                        required=True, metavar="path")
    args = parser.parse_args()

    return args.path


# ---------------------Get Files From Valid Path-------------------
def get_file_paths(root, file_list):
    """
    Return a list of all files inside a single directory
    specify by an absolute path.

    @param root: An absolute path of a directory.

    @param file_list: A list of files inside a directory.

    @return: a list of files with absolute paths.
    """
    files = []
    for file_name in file_list:
        file_path = join(root, file_name)
        # Skip the symlink file
        if not islink(file_path):
            files.append(abspath(file_path))

    return files


def scan_files(path):
    """
    Return the complete list of all files inside all directory
    specify by an absolute path.

    @param path: An absolute path of a directory.

    @return: a list of files with absolute paths.
    """
    files = []
    for root, _, file_list in walk(path):
        files += get_file_paths(root, file_list)

    return files


# ---------------------Grouping Based On File-size-----------------
def create_size_dict(file_path_names):
    """
    Return a dictionary of files with key is the size and
    value is the filepath which has that size.

    @param file_path_names: A list of files with absolute paths.

    @return: A dictionary of sizes and filepaths.
    """
    size_dict = {}
    # Create a dict with key is the filesize and
    # values are the filepath
    for file in file_path_names:
        file_size = getsize(file)
        # if file is empty
        if file_size == 0:
            continue
        # if size already added in dict
        elif file_size in size_dict:
            size_dict[file_size].append(file)
        # if size haven't been added in dict
        else:
            size_dict[file_size] = [file]

    return size_dict


def group_files_by_size(file_path_names):
    """
    Return a list of groups of files with the same size.

    @param file_path_names: A list of files with absolute paths.

    @return: a list of groups of files.
    """
    size_list = []
    size_dict = create_size_dict(file_path_names)
    # Create a list of groups of files that have more
    # than 2 items
    for group in size_dict.values():
        if len(group) > 1:
            size_list.append(group)

    return size_list


# ---------------------Convert Content to Checksum-----------------
def get_file_checksum(file):
    """
    Get the hash value from a file's content.

    @param file: A file's absolute path.

    @return: The hash value of a file.
    """
    # Error handling if file has no permission to read.
    if not access(file, R_OK):
        return None
    else:
        with open(file, 'rb') as data:
            file_hash = md5(data.read()).hexdigest()

        return file_hash


# ---------------------Grouping Based on Checksum------------------
def create_hash_dict(file_path_names):
    """
    Return a dictionary with key is the hash and value is the filepath with
    that hash.

    @param file_path_names: A list of files with absolute paths.

    @return: A dictionary of hashes and filepaths.
    """
    hash_dict = {}
    # Create a dict with key is the filehash and
    # values are the filepath
    for file in file_path_names:
        file_hash = get_file_checksum(file)
        # if the file_hash is not None
        if file_hash:
            if file_hash in hash_dict:
                hash_dict[file_hash].append(file)
            else:
                hash_dict[file_hash] = [file]

    return hash_dict


def group_files_by_checksum(file_path_names):
    """
    Return a list of group of files with the same checksum.

    @param file_path_names: A list of files with absolute paths.
    The list being passed in will be sorted by size beforehand for efficiency.

    @return: A list of groups of files.
    """
    hash_list = []
    hash_dict = create_hash_dict(file_path_names)
    # Create a list of groups of files that have more
    # than 2 items
    for group in hash_dict.values():
        if len(group) > 1:
            hash_list.append(group)

    return hash_list


# --------Find Duplicate Files Based on Size and Checksum----------
def find_duplicate_files(file_path_names):
    """
    Return a list of groups of duplicates filtered by size and checksum.

    @param file_path_names: A list of files with absolute paths.

    @return: A list of groups of duplicates.
    """
    groups = []
    # Grouping files by size first
    size_list = group_files_by_size(file_path_names)
    # Grouping each group by checksum
    for group in size_list:
        hash_list = group_files_by_checksum(group)
        groups += hash_list

    return groups


# ---------------------------Main Function-------------------------
def main():
    """
    Entry point of the script.
    Convert the result into JSON formatted string.
    """
    try:
        path = get_argument()
        # Error handling when the path don't exists or is a file
        if not exists(path) or isfile(path):
            print("Invalid path")
            exit(1)
        else:
            # Get the list of files inside the directory specified by the path
            file_path_names = scan_files(path)
            # Return a list of groups of duplicate files
            data = find_duplicate_files(file_path_names)
            # Print out to JSON formatted string
            print(dumps(data))
    except Exception:
        print("Check the directory or the input again!")
        exit(1)


if __name__ == "__main__":
    main()
