#!/usr/bin/env python3

from os.path import join, exists, isfile, islink, getsize, abspath
from argparse import ArgumentParser
from hashlib import md5
from json import dumps
from os import walk


#---------------------Get Argument From User----------------------
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


#---------------------Get Files From Valid Path-------------------
def scan_files(path):
    """
    Return the complete list of all files inside a directory
    specify by an absolute path.

    @param path: An absolute path of a directory.

    @return: a list of files with absolute paths.
    """
    files=[]
    for root, _, file in walk(path):
        for file_name in file:
            file_path = join(root, file_name)
            # Skip the symlink file
            if not islink(file_path):
                files.append(abspath(file_path))
    
    return files


#---------------------Grouping Based On File-size-----------------
def group_files_by_size(file_path_names):
    """
    Return a list of groups of files with the same size.

    @param file_path_names: A list of files with absolute paths.

    @return: a list of groups of files.
    """
    group_dict = {}
    group_list = []
    
    # Create a dict with key is the filesize and
    # values are the filepath
    for file in file_path_names:
        file_size = getsize(file)
        if file_size == 0:
            continue
        elif file_size in group_dict:
            group_dict[file_size].append(file)
        else:
            group_dict[file_size] = [file]
    
    # Create a list of groups of files that have more 
    # than 2 items (might store duplicates inside)
    for group in group_dict.values():
        if len(group) > 1:
            group_list.append(group)

    return group_list


#---------------------Convert Content to Checksum-----------------
def get_file_checksum(file):
    """
    Get the hash value from a file's content.

    @param file: A file's absolute path.

    @return: The hash value of a file.
    """
    with open(file, 'rb') as data:
        file_hash = md5(data.read()).hexdigest()
    
    return file_hash


#---------------------Grouping Based on Checksum------------------
def group_files_by_checksum(file_path_names):
    """
    Return a list of group of files with the same checksum.

    @param file_path_names: A list of files with absolute paths.
    The list being passed in will be sorted by size beforehand for efficiency.

    @return: A list of groups of files.
    """
    group_dict = {}
    group_list = []
    # Create a dict with key is the filehash and
    # values are the filepath
    for file in file_path_names:
        file_hash = get_file_checksum(file)
        if file_hash in group_dict:
            group_dict[file_hash].append(file)
        else:
            group_dict[file_hash] = [file]
    # Create a list of groups of files that have more
    # than 2 items (might store duplicates inside)
    for group in group_dict.values():
        if len(group) > 1:
            group_list.append(group)

    return group_list


#--------Find Duplicate Files Based on Size and Checksum----------
def find_duplicate_files(file_path_names):
    groups = []

    size_groups = group_files_by_size(file_path_names)
    for group in size_groups:
        group = group_files_by_checksum(group)
        groups += group

    return groups


#---------------------------Main Function-------------------------
def main():
    path = get_argument()
    if not exists(path) or isfile(path):
        print("Invalid path")
        exit(1)
    else:
        file_path_names = scan_files(path)
        data = find_duplicate_files(file_path_names)
        print(dumps(data))


if __name__ == "__main__":
    main()
