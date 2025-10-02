import argparse
import os
import git
import io
import sys
import time
import logging

try:
    import tomllib  # Python 3.11+
    def toml_load_file(path):
        with open(path, "rb") as f:
            return tomllib.load(f)
except Exception:
    try:
        import toml
        def toml_load_file(path):
            with open(path, "r", encoding="utf-8") as f:
                return toml.load(f)
    except Exception:
        toml_load_file = None


## Global Variables ###############################################################################
parser = argparse.ArgumentParser()
version_num = "0.1.0"
file_count = 0
line_count = 0
MAX_FILE_BYTES = 16 * 1024 # 16KB
RECENT_DAY = 3000 / (60*60*24)
CONFIG_FILE = ".repo-scan-config.toml"

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

parser.add_argument(
    "-r", "--recent",
    help="Include only recently modified files (in the last 7 days)",
    action="store_true"
    )

parser.add_argument(
    "-vb", "--verbose",
    help="Enable detailed progress information",
    action="store_true"
    )

## Config loader #################################################################################
def load_config_file(config_name=CONFIG_FILE):
    """
    Load config from a TOML file in the current working directory.
    - If file does not exist: returns empty dict.
    - If file exists but cannot be parsed: exit with error.
    - Returns only recognized keys.
    """
    if toml_load_file is None:
        # toml not available: will continue without config, but inform user in verbose mode
        return {}

    config_path = os.path.join(os.getcwd(), config_name)
    if not os.path.exists(config_path):
        return {}

    try:
        parsed = toml_load_file(config_path)
    except Exception as e:
        # clear error message and exit (requirement)
        logging.error("Failed to parse TOML config %s: %s", config_path, e)
        sys.exit(2)

    if not isinstance(parsed, dict):
        return {}

    # Recognized keys: only accept known ones (ignore unknown keys)
    recognized = {"output", "recent", "verbose", "paths", "max_file_size"}
    filtered = {}
    for k, v in parsed.items():
        if k in recognized:
            filtered[k] = v
    return filtered


## Functions ######################################################################################
def analyze_path_args(args):
    

    directories = []
    filenames = []

    # Determine if argument is a directory path or a filename
    for path in args.paths:
        absolute_path = os.path.normpath(os.path.abspath(path))

        if os.path.isdir(absolute_path):
            directories.append(absolute_path)
        else:
            filenames.append(path)
    
    # Enforce only one directory and seperate directory and filename arguments
    if len(directories) > 1:
        logging.error("Only one directory path is allowed.")
        sys.exit(1)
    elif len(directories) > 0 and len(filenames) > 0:
        logging.error("Please enter only a single directory path OR one or more filenames.")
        sys.exit(1)

    # Directory output
    if (directories):
        logging.info("Analyzing directory: %s", directories[0])
        content_output(directories[0], args.recent, None, args.output)

    # File output
    elif (filenames):
        # Use current directory to search filenames
        search_dir = os.getcwd()
        logging.info("Searching in directory: %s", search_dir)


        # Find filenames in current directory
        for name in filenames:
            for root, _, files in os.walk(search_dir):
                if name in files:
                    logging.info("Found %s in %s", name, root)
                else:
                    logging.error("%s not found.", name)
                    sys.exit(1)
        
        content_output(search_dir, args.recent, filenames, args.output)

def is_recently_modified(file_path, recent_day=RECENT_DAY):
    logging.info("Checking file: %s", file_path)
    try:
        file_stats = os.stat(file_path)
        last_modified_time = file_stats.st_mtime
        current_time = time.time()

        time_difference = current_time - last_modified_time
        days_difference = time_difference / (60 * 60 * 24)

        logging.info("Last modified: %.2f days ago", days_difference)

        return days_difference <= recent_day
    except FileNotFoundError as e:
        logging.error("OS error while checking %s: %s", file_path, e)
        return False

def content_output(absolute_path, contain_recent_files_only, filenames=None, output=None):
    global file_count, line_count
    buffer = io.StringIO()

    logging.info("Starting content output for path: %s", absolute_path)

    # Repository context
    buffer.write(f"# Repository Context\n\n")

    buffer.write(f"## File System Location\n\n")
    buffer.write(f"{absolute_path}\n\n")

    # Git info
    buffer.write(f"## Git Info\n\n")
    git_info = pull_git_info(absolute_path)
    if git_info:
        buffer.write(f"{git_info}\n\n")
    else:
        buffer.write(f"Not a git repository\n\n")

    # Structure
    buffer.write(f"## Structure\n")
    structure = analyze_structure(absolute_path)
    buffer.write("```\n")
    buffer.write(f"{structure}\n")
    buffer.write("```\n\n")

    # File contents
    buffer.write("## File Contents\n")
    if contain_recent_files_only:
        buffer.write("[Only the recently modified files would be included here]\n\n")
        logging.info("Filtering for recently modified files only.")
    else:
        buffer.write("\n")
        logging.info("Including all files.")

    if filenames:
        if contain_recent_files_only:
            file_paths = [file for file in filenames if is_recently_modified(file, RECENT_DAY)]
        else:
            file_paths = filenames
        logging.info("Using provided filenames: %d files", len(file_paths))
    else:
        if contain_recent_files_only:
            file_paths = [file for file in list_all_files(absolute_path) if is_recently_modified(file, RECENT_DAY)]
        else:
            file_paths = list_all_files(absolute_path)

    if len(file_paths) == 0:
        buffer.write("No file content available.\n\n")
        logging.info("No files matched the criteria.")

    for file_path in file_paths:
        filename = os.path.basename(file_path)

        # Only print modified time if recent flag is True
        if contain_recent_files_only:
            try:
                time_seconds = os.path.getmtime(file_path)
                modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_seconds))
            except Exception as e:
                logging.error("Could not retrieve modification time for %s: %s", file_path, e)
                modified_time = "Unknown"
            buffer.write(f"### File: {filename} (Modified: {modified_time})\n")
        else:
            buffer.write(f"### File: {filename}\n")

        buffer.write("```\n")
        buffer.write(analyze_file_content(file_path))
        buffer.write("\n```\n\n")

    # Summary
    buffer.write("## Summary\n")
    if contain_recent_files_only:
        buffer.write(f"- Total files(recently changed): {len(file_paths)}\n")
    else:
        if filenames:
            file_count = len(filenames)
        buffer.write(f"- Total files: {file_count}\n")
    buffer.write(f"- Total lines: {line_count}\n\n")

    content = buffer.getvalue()

    if output:
        logging.info("Writing results to file: %s", output)
        write_results(content, output)
    else:
        logging.info("Displaying results to terminal.")
        print("Displaying results..\n")
        print(content)
 

def pull_git_info(absolute_path):
    try:
        logging.info("Attempting to retrieve Git info from: %s", absolute_path)
        repo = git.Repo(absolute_path)

        # Get the latest commit
        commit = repo.head.commit
        logging.info("Latest commit hash: %s", commit.hexsha)

        # Get current branch
        branch = repo.active_branch.name
        logging.info("Active branch: %s", branch)

        # Output
        logging.info("Git info successfully retrieved for %s", absolute_path)
        return (
            f"- Commit: {commit.hexsha}\n"
            f"- Branch: {branch}\n"
            f"- Author: {commit.author.name} <{commit.author.email}>\n"
            f"- Date: {commit.committed_datetime.strftime('%a %b %d %H:%M:%S %Y %z')}"
        )

    except git.exc.InvalidGitRepositoryError:
        logging.warning("No valid Git repository found at: %s", absolute_path)
        return None
    except Exception as e:
        logging.error("Unexpected error while retrieving Git info from %s: %s", absolute_path, e)
        return None


def analyze_structure(absolute_path):
    output = []
    logging.info("Analyzing directory structure at: %s", absolute_path)

    for dirpath, dirnames, filenames in os.walk(absolute_path):
        # Skip .git directory
        if ".git" in dirnames:
            dirnames.remove(".git")
            logging.info("Skipping .git directory in: %s", dirpath)

        depth = dirpath.replace(absolute_path, "").count(os.sep)
        indent = "  " * depth

        # Add subdirectory
        dirname = os.path.basename(dirpath) or absolute_path
        output.append(f"{indent}{dirname}/")
        logging.info("Found directory: %s", dirname)

        # Add files
        for filename in filenames:
            output.append(f"{indent}  {filename}")
            logging.info("Found file: %s in %s", filename, dirpath)

    logging.info("Finished analyzing structure for: %s", absolute_path)
    return "\n".join(output)


def analyze_file_content(file_path):
    global line_count
    try:
        logging.info("Analyzing file: %s", file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_FILE_BYTES + 1)

        lines = content.splitlines()
        line_count += len(lines)
        logging.info("File %s has %d lines (running total: %d)",
                     file_path, len(lines), line_count)

        escaped_lines = []
        for line in lines:
            # Replace triple backticks to keep markdown output clean
            escaped_line = line.replace("```", "&#96;&#96;&#96;")
            escaped_lines.append(escaped_line)

        result = "\n".join(escaped_lines)

        if len(content.encode("utf-8")) > MAX_FILE_BYTES:
            logging.info("File %s exceeds %d bytes, truncating output.",
                         file_path, MAX_FILE_BYTES)
            result += "\n\n[Truncated: file exceeds 16KB limit]"
        else:
            logging.info("File %s processed successfully.", file_path)

        return result

    except Exception as e:
        logging.error("Failed to read %s: %s", file_path, e)
        return f"Failed to read {file_path}: {e}"


def list_all_files(absolute_path):
    global file_count
    file_paths = []

    logging.info("Listing all files under: %s", absolute_path)

    for root, dirs, files in os.walk(absolute_path):
        # Skip .git directory and its contents
        if ".git" in dirs:
            dirs.remove(".git")
            logging.info("Skipping .git directory in: %s", root)

        for file in files:
            # Skip hidden files
            if file.startswith("."):
                logging.info("Skipping hidden file: %s in %s", file, root)
                continue

            full_path = os.path.join(root, file)
            file_paths.append(full_path)
            file_count += 1
            logging.info("Discovered file: %s", full_path)

    logging.info("Finished listing files. Total files found: %d", file_count)
    return file_paths


def write_results(content, output):
    try:
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info("Results successfully written to %s", output)
    except Exception as e:
        logging.error("Failed to write to %s: %s", output, e)


if __name__ == "__main__":        
    # Parse CLI args
    args = parser.parse_args()

    # Load config from TOML (if present)
    config = load_config_file()

    # If TOML package is required and not present, we still continue but notify user when verbose
    if toml_load_file is None:
        # No toml support available: user must have installed dependency to use config file
        if args.verbose:
            logging.warning("TOML support not found. Install 'toml' package to enable config file support.")

    # Merge values: config provides defaults, CLI overrides config
   # -- output
    if args.output is None and "output" in config:
        args.output = config["output"]

    
# Recent
    if not args.recent and "recent" in config:
        # Convert only if it is actual bool; otherwise treat as False
        if isinstance(config["recent"], bool):
            args.recent = config["recent"]
        else:
            args.recent = str(config["recent"]).lower() == "true"

    # -- verbose  
    if not args.verbose and "verbose" in config:
        if isinstance(config["verbose"], bool):
            args.verbose = config["verbose"]
        else:
            if str(config["verbose"]).lower() == "true":
                args.verbose = True
            else:
                args.verbose = False

    # -- paths 
    if not args.paths and "paths" in config:
        if isinstance(config["paths"], list):
            args.paths = config["paths"]
        else:
            args.paths = [config["paths"]]

    # -- max_file_size
    if "max_file_size" in config:
        try:
            val = int(config["max_file_size"])
            if val > 0:
                MAX_FILE_BYTES = val
        except Exception:
            logging.warning("Invalid max_file_size in config; ignoring.")

    # If still no paths provided, default to current directory
    if not args.paths:
        args.paths = [os.getcwd()]

    # Configure logging now that verbose setting is known
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s"
    )

    analyze_path_args(args)