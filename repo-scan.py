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
    elif os.path.isfile(absolute_path):
        print(f"Analyzing file: {absolute_path}")
    else:
        print(f"Invalid path: {absolute_path}")

args = parser.parse_args()

for path in args.paths:
    analyze_args(path)