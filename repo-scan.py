import argparse
import os

parser = argparse.ArgumentParser()
version_num = "0.1.0"

parser.add_argument(
    "-v", "--version", 
    help="Displays tool name and version number",
    action="version",
    version=f"Repository Context Packager {version_num}"
    )

parser.add_argument(
    "paths",
    nargs="*",
    help="Directory path or files to analyze. Defaults to current directory."
    )

def analyze_args(arg):
    absolute_path = os.path.abspath(arg)

    if os.path.isdir(absolute_path):
        print(f"Analyzing directory: {absolute_path}")
        display_file_structure(absolute_path)
    elif os.path.isfile(absolute_path):
        print(f"Analyzing file: {absolute_path}")
    else:
        print(f"Invalid path: {absolute_path}")

def display_file_structure(absolute_path):
    print(f"\nFile Structure:\n")

    for dirpath, dirnames, filenames in os.walk(absolute_path):
        depth = dirpath.replace(absolute_path, "").count(os.sep)
        indent = "    " * depth
        print(f"{indent}📂 {os.path.basename(dirpath) or absolute_path}")

        # Print subdirectories
        for dirname in dirnames:
            print(f"{indent}    📁 {dirname}")

        # Print files
        for filename in filenames:
            print(f"{indent}    📄 {filename}")


args = parser.parse_args()

for path in args.paths:
    analyze_args(path)