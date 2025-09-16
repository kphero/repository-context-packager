import argparse
import os
import git
import io
import sys

## Global Variables ###############################################################################
parser = argparse.ArgumentParser()
version_num = "0.1.0"
file_count = 0
line_count = 0
MAX_FILE_BYTES = 16 * 1024 # 16KB

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
def analyze_path_args(paths):
    directories = []
    filenames = []

    # Determine if argument is a directory path or a filename
    for path in paths:
        absolute_path = os.path.normpath(os.path.abspath(path))

        if os.path.isdir(absolute_path):
            directories.append(absolute_path)
        else:
            filenames.append(path)
    
    # Enforce only one directory and seperate directory and filename arguments
    if len(directories) > 1:
        print("ERROR: Only one directory path is allowed.", file=sys.stderr)
        sys.exit(1)
    elif len(directories) > 0 and len(filenames) > 0:
        print("ERROR: Please enter only a single directory path OR one or more filenames.", file=sys.stderr)
        sys.exit(1)

    # Directory output
    if (directories):
        print(f"Analyzing directory: {directories[0]}")
        content_output(directories[0], None, args.output)

    # File output
    elif (filenames):
        # Use current directory to search filenames
        search_dir = os.getcwd()
        print(f"Searching in directory: {search_dir}") 

        # Find filenames in current directory
        for name in filenames:
            for root, _, files in os.walk(search_dir):
                if name in files:
                    print(f"Found {name} in {search_dir}...")
                else:
                    print(f"ERROR: {name} not found.", file=sys.stderr)
                    sys.exit(1)
        
        content_output(search_dir, filenames, args.output)

def content_output(absolute_path, filenames=None, output=None):
    global file_count, line_count
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

    buffer.write(f"## Structure\n")
    structure = analyze_structure(absolute_path)
    buffer.write("```\n")
    buffer.write(f"{structure}\n")
    buffer.write("```\n\n")

    buffer.write("## File Contents\n\n")
    if (filenames):
        file_paths = filenames
    else:
        file_paths = list_all_files(absolute_path)

    for file_path in file_paths:
        filename = os.path.basename(file_path)

        buffer.write(f"### File: {filename}\n")
        buffer.write("```\n")
        buffer.write(analyze_file_content(file_path))
        buffer.write("\n```\n\n")

    buffer.write("## Summary\n")
    if (filenames):
        file_count = len(filenames)
    buffer.write(f"- Total files: {file_count}\n")
    buffer.write(f"- Total lines: {line_count}\n\n")

    content = buffer.getvalue()

    if output:
        print(f"Writing results to {output}..")
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
    global file_count
    output = []

    for dirpath, dirnames, filenames in os.walk(absolute_path):
        if ".git" in dirnames:
            dirnames.remove(".git")

        depth = dirpath.replace(absolute_path, "").count(os.sep)
        indent = "  " * depth

        # Print subdirectory
        output.append(f"{indent}{os.path.basename(dirpath) or absolute_path}/")

        # Print files
        for filename in filenames:
            output.append(f"{indent}  {filename}")
            file_count += 1

    return "\n".join(output)

def analyze_file_content(file_path):
    global line_count
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_FILE_BYTES + 1)

            lines = content.splitlines()
            line_count += len(lines)

            escaped_lines = []
            for line in lines:
                # Replace triple backticks to keep markdown output clean
                escaped_line = (line.replace("```", "&#96;&#96;&#96;"))
                escaped_lines.append(escaped_line)

            result = "".join(escaped_lines)

            if len(content.encode("utf-8")) > MAX_FILE_BYTES:
                result += "\n\n[Truncated: file exceeds 16KB limit]"

            return result

    except Exception as e:
        return f"Failed to read {file_path}: {e}"

def list_all_files(absolute_path):
    file_paths = []
    for root, dirs, files in os.walk(absolute_path):
        # Skip .git directory and its contents
        dirs[:] = [d for d in dirs if d != ".git"]

        for file in files:
            # Skip hidden Git files
            if root.endswith(".git"):
                continue

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

    analyze_path_args(args.paths)