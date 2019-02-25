#!/usr/bin/env python3
from argparse import ArgumentParser
from os import walk
from os.path import join, exists, isfile


def get_argument():
    parser = ArgumentParser(prog="Duplicate Files Finder",
                            description="Finding Duplicates")
    parser.add_argument('-p', '--path', type=str, required=True, 
                        metavar="path", dest="path")
    args = parser.parse_args()
    return args.path


def scan_files(path, file_list=set()):
    for root, dirs, files in walk(path):
        for file in files:
            file_list.add(join(root, file))
        for dir in dirs:
            file_list = scan_files(join(root, dir), file_list)
    return file_list


if __name__ == "__main__":
    path = get_argument()
    if not exists(path):
        print("Invalid path")
        exit(1)
    else:
        file_list = scan_files(path)
        print(file_list)
