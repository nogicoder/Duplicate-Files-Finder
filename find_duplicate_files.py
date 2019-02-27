#!/usr/bin/env python3
from argparse import ArgumentParser
from os import walk
from os.path import join, exists, isfile, islink, getsize
from hashlib import md5
from json import dumps


def get_argument():
    parser = ArgumentParser(prog="Duplicate Files Finder",
                            description="Finding Duplicates")
    parser.add_argument('-p', '--path', type=str, required=True, 
                        metavar="path", dest="path")
    args = parser.parse_args()
    return args.path


def scan_files(path, file_list=[]):
    for root, dirs, files in walk(path):
        for file in files:
            file_path = join(root, file)
            if file_path not in file_list:
                file_list.append(file_path)
        for dir in dirs:
            dir_path = join(root, dir)
            if not islink(dir_path):
                file_list = scan_files(dir_path, file_list)
    return file_list


def group_files_by_size(file_path_names):

    def get_size_list(file_path_names):
        size_list = []
        for file in file_path_names:
            file_size = getsize(file)
            if file_size and file_size not in size_list:
                size_list.append(file_size)
        return size_list

    groups = []
    size_list = get_size_list(file_path_names)

    for size in size_list:
        group = []
        for file in file_path_names:
            file_size = getsize(file)
            if file_size == size:
                group.append(file)
        if len(group) > 1:
            groups.append(group)
            
    return groups


def group_files_by_checksum(file_path_names):

    def get_file_checksum(file_path_names):
        hash_list = []
        for file in file_path_names:
            with open(file) as f:
                file_hash = md5(f.read().encode()).hexdigest()
                if file_hash not in hash_list:
                    hash_list.append(file_hash)
        return hash_list

    groups = []
    hash_list = get_file_checksum(file_path_names)
    
    for hash in hash_list:
        group = []
        for file in file_path_names:
            with open(file) as f:
                file_hash = md5(f.read().encode()).hexdigest()
                if file_hash == hash:
                    group.append(file)
        if len(group) > 1:
            groups.append(group)

    return groups


def find_duplicate_files(file_path_names):
    size_groups = group_files_by_size(file_path_names)
    groups = []
    for group in size_groups:
        group = group_files_by_checksum(group)
        if group:
            groups += group

    return groups 


def main():
    path = get_argument()
    if not exists(path):
        print("Invalid path")
        exit(1)
    else:
        file_list = scan_files(path)
        data = find_duplicate_files(file_list)
        print(dumps(data))


if __name__ == "__main__":
    main()