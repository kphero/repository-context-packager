import argparse
import os
import git

parser = argparse.ArgumentParser()
version_num = "0.1.0"

parser.add_argument(
    "-v", "--version", 
    help="Displays tool name and version number",
    action="version",
    version=f"Repository Context Packager {version_num}"
    )

parser.add_argument(
    "-o", "--output", 
    type=str,
    help="Package results will be written to JSON file",
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
        content_output(absolute_path)
    elif os.path.isfile(absolute_path):
        print(f"Analyzing file: {absolute_path}")
        content_output(absolute_path)
    else:
        print(f"Invalid path: {absolute_path}")

def content_output(absolute_path):
    print(f"# Repository Context\n")

    print(f"## File System Location\n")
    print(absolute_path)

    print(f"\n## Git Info\n")
    pull_git_info(absolute_path)

    print(f"## Structure\n")
    analyze_structure(absolute_path)

def pull_git_info(absolute_path):
    repo = git.Repo(absolute_path)

    # Get the latest commit
    commit = repo.head.commit

    # Get current branch
    branch = repo.active_branch.name

    # Output
    print(f"- Commit: {commit.hexsha}")
    print(f"- Branch: {branch}")
    print(f"- Author: {commit.author.name} <{commit.author.email}>")
    print(f"- Date: {commit.committed_datetime.strftime('%a %b %d %H:%M:%S %Y %z')}\n")


def analyze_structure(absolute_path):
    for dirpath, dirnames, filenames in os.walk(absolute_path):
        depth = dirpath.replace(absolute_path, "").count(os.sep)
        indent = "  " * depth
        print(f"{indent}{os.path.basename(dirpath) or absolute_path}/")

        # Print subdirectories
        for dirname in dirnames:
            print(f"{indent}  {dirname}/")

        # Print files
        for filename in filenames:
            print(f"{indent}  {filename}")

def write_results(output, content):
    try:
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)
            print(f"Results written to {output}")
    except Exception as e:
        print(f"Failed to write to {output}: {e}")
args = parser.parse_args()

for path in args.paths:
    analyze_args(path)