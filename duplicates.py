import sys
import os
import argparse
from collections import (
    namedtuple,
    defaultdict
)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-dir",
        help="Please provide a file to catalog",
        type=str,
        required=True
    )
    return parser


def get_descriptions_of_files_from_directory(directory_path):
    FileDescription = namedtuple("File", "name, size")
    found_files = defaultdict(list)

    for root, dirs, file_names in os.walk(directory_path):
        for name in file_names:
            full_file_path = os.path.join(root, name)

            file_description = FileDescription(
                name,
                os.path.getsize(full_file_path)
            )

            found_files[file_description].append(root)

    return found_files


def find_duplicates(files_from_directory):
    duplicates = {}
    for file_description, file_names in files_from_directory.items():
        if len(file_names) > 1:
            duplicates[file_description] = file_names
    return duplicates


if __name__ == "__main__":
    parser = create_parser()

    args = parser.parse_args()

    if not os.path.exists(args.dir):
        sys.exit("Directory {} does not exists.".format(args.dir))

    files_from_directory = get_descriptions_of_files_from_directory(args.dir)
    duplicates_of_files = find_duplicates(files_from_directory)

    for file_description, file_paths in duplicates_of_files.items():
        print(
            "name: {}, size: {}, locations:".format(
                file_description.name,
                file_description.size
            )
        )
        for file_path in file_paths:
            print("".join(["\t", file_path]))
