import argparse
import os
import git
import io
import sys

## Global Variables ###############################################################################
parser = argparse.ArgumentParser()
version_num = "0.1.0"

## Parser Arguments ###############################################################################
parser.add_argument(
    "-v", "--version", 
    help="Displays tool name and version number",
    action="version",
    version=f"Repository Context Packager {version_num}"
    )

parser.add_argument(
    "-o", "--output", 
    nargs="?",
    const="output.txt",
    default=None,
    type=str,
    help="Package results will be written to file (default: output.txt if no filename is given)",
    )

parser.add_argument(
    "paths",
    nargs="*",
    help="Directory path or files to analyze. Defaults to current directory."
    )

## Functions ######################################################################################
def analyze_args(arg):
    absolute_path = os.path.normpath(os.path.abspath(arg))
    
    if os.path.isdir(absolute_path):
        print(f"Analyzing directory: {absolute_path}")
        content_output(absolute_path, args.output)
    elif os.path.isfile(absolute_path):
        print(f"Analyzing file: {absolute_path}")
        content_output(absolute_path, args.output)
    else:
        print(f"Invalid path: {absolute_path}")

def content_output(absolute_path, output=None):
    # Write to buffer then determine if output is displayed in terminal or in file
    buffer = io.StringIO()

    buffer.write(f"# Repository Context\n\n")

    buffer.write(f"## File System Location\n\n")
    buffer.write(f"{absolute_path}\n\n")

    buffer.write(f"## Git Info\n\n")
    git_info = pull_git_info(absolute_path)
    if git_info:
        buffer.write(f"{git_info}\n\n")
    else:
        buffer.write(f"Not a git repository\n\n")

    buffer.write(f"## Structure\n\n")
    structure = analyze_structure(absolute_path)
    buffer.write("```\n")
    buffer.write(f"{structure}\n")
    buffer.write("\n```\n\n")

    buffer.write("## File Contents\n\n")
    file_paths = list_all_files(absolute_path)

    for file_path in file_paths:
        filename = os.path.basename(file_path)

        buffer.write(f"### File: {filename}\n")
        buffer.write("```\n")
        buffer.write(analyze_file_content(file_path))
        buffer.write("\n```\n\n")

    content = buffer.getvalue()

    if output:
        print(f"Writing results to {output}..\n")
        write_results(content, output)
    else:
        print("Displaying results..\n")
        print(content) 

def pull_git_info(absolute_path):
    try:
        repo = git.Repo(absolute_path)

        # Get the latest commit
        commit = repo.head.commit

        # Get current branch
        branch = repo.active_branch.name

        # Output
        return(
            f"- Commit: {commit.hexsha}\n"
            f"- Branch: {branch}\n"
            f"- Author: {commit.author.name} <{commit.author.email}>\n"
            f"- Date: {commit.committed_datetime.strftime('%a %b %d %H:%M:%S %Y %z')}"
        )
    except git.exc.InvalidGitRepositoryError:
        return None

def analyze_structure(absolute_path):
    output = []

    for dirpath, dirnames, filenames in os.walk(absolute_path):
        if ".git" in dirnames:
            dirnames.remove(".git")

        depth = dirpath.replace(absolute_path, "").count(os.sep)
        indent = "  " * depth

        output.append(f"{indent}{os.path.basename(dirpath) or absolute_path}/")

        # Print subdirectories
        for dirname in dirnames:
            output.append(f"{indent}  {dirname}/")

        # Print files
        for filename in filenames:
            output.append(f"{indent}  {filename}")

    return "\n".join(output)

def analyze_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Failed to read {file_path}: {e}"


def list_all_files(absolute_path):
    file_paths = []
    for root, _, files in os.walk(absolute_path):
        for file in files:
            full_path = os.path.join(root, file)
            file_paths.append(full_path)
    return file_paths



def write_results(content, output):
    try:
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)
            print(f"Results successfully written to {output}")
    except Exception as e:
        print(f"Failed to write to {output}: {e}")

if __name__ == "__main__":        
    args = parser.parse_args()

    if len(sys.argv) == 1:
        print("ERROR: No arguments provided.\n")
        parser.print_help(sys.stderr)
        sys.exit(1)

    for path in args.paths:
        analyze_args(path)