#!/usr/bin/python3

import argparse
import json
import logging
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path


def delete_file(file_path):
    os.remove(file_path)
    return True


def get_file_or_folder_age(path):
    # getting ctime of the file/folder
    # time will be in seconds
    ctime = os.stat(path).st_atime

    # returning the time
    return ctime


def cleanup(paths, filters, args):
    for path in paths:
        cleanup_dir(path, filters, args)


# cleanup function
def cleanup_dir(path, filters, args):
    # checking whether the path exist or not
    if os.path.exists(path):

        # check whether the path is directory or not
        if os.path.isdir(path):

            # iterating through the subfolders
            for root_folder, folders, files in os.walk(path):

                # checking of the files
                for file in files:

                    # file path
                    file_path = os.path.join(root_folder, file)

                    is_removable = True

                    for callback in filters:
                        is_removable = is_removable and callback(file_path, args)

                    if is_removable:
                        # deleting the file
                        if delete_file(file_path):

                            # success message
                            print(f"{file_path} deleted successfully")

                        else:

                            # failure message
                            print(f"Unable to delete the {file_path}")
                    else:
                        print(f"skip {file_path}")

        else:
            # path is not a directory
            print(f"{path} is not a directory")

    else:

        # path doesn't exist
        print(f"{path} doesn't exist")


def days_filter(file_path, args):
    time_point = time.time() - (args.days * 24 * 60 * 60)

    if get_file_or_folder_age(file_path) < time_point:
        return True

    return False


def extension_filter(file_path, args):
    # extracting the extension from the filename
    file_extension = os.path.splitext(file_path)[1]

    # checking the file_extension
    if args.extension == file_extension:
        return True

    return False


def get_args():
    my_parser = argparse.ArgumentParser(description='cleanup util to remove files with certain filters')
    # Add the arguments
    my_parser.add_argument('--paths',
                           type=list,
                           default=['./2', './3'],
                           help='multiple list of directories for cleanup')
    my_parser.add_argument('--days',
                           type=int,
                           default=60,
                           help='number of days old for files to cleanup')
    my_parser.add_argument('--extension',
                           type=str,
                           default='.log',
                           help='file extension filter to cleanup')

    return my_parser.parse_args()


def main():
    args = get_args()
    print(f"{args.paths} {args.days} {args.extension}")

    filters = [days_filter, extension_filter]

    cleanup(args.paths, filters, args)


if __name__ == '__main__':
    # invoking main function
    main()

# python3 cleanup_util.py
# python3 cleanup_util.py --help
