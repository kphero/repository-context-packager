import os
import time
import logging

def is_recently_modified(file_path: str, recent_day: int = 7) -> bool:
    """
    Check if a file was modified within the last `recent_day` days.

    Args:
        file_path: Path to the file.
        recent_day: Number of days to consider as "recent".

    Returns:
        True if the file was modified within the threshold, False otherwise.
    """

    try:
        # Get the last modification time of the file (in seconds since epoch)
        last_modified_time = os.stat(file_path).st_mtime

        # Calculate how many days ago the file was modified
        days_difference = (time.time() - last_modified_time) / (60 * 60 * 24)

        # Return True if the file was modified within the recent_day threshold
        return days_difference <= recent_day

    except FileNotFoundError as e:
        logging.error("OS error while checking %s: %s", file_path, e)
        return False


def analyze_file_content(file_path: str, max_bytes: int) -> tuple[str, int]:
    """
    Read and sanitize the content of a file, up to a byte limit.

    Args:
        file_path: Path to the file.
        max_bytes: Maximum number of bytes to read.

    Returns:
        A tuple containing:
            - Sanitized string content (with triple backticks escaped).
            - Number of lines read.
    """

    try:
        # Open the file in UTF-8 encoding and read slightly more than max_bytes
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(max_bytes + 1)

        # Split content into lines
        lines = content.splitlines()

        # Escape any triple backticks to avoid breaking markdown formatting
        escaped_lines = [line.replace("```", "&#96;&#96;&#96;") for line in lines]

        # Rejoin lines into a single string
        result = "\n".join(escaped_lines)

        # Check if the file exceeds the byte limit (after encoding)
        truncated = len(content.encode("utf-8")) > max_bytes
        if truncated:
            result += f"\n\n[Truncated: file exceeds {max_bytes//1024}KB limit]"

        # Return sanitized content and line count
        return result, len(lines)

    except Exception as e:
        logging.error("Failed to read %s: %s", file_path, e)
        return f"Failed to read {file_path}: {e}", 0


def list_all_files(absolute_path: str, include_hidden: bool = False) -> list[str]:
    """
    Recursively list all files in a directory, excluding .git, __pycache__, and optionally hidden files.

    Args:
        absolute_path: Root directory to scan.
        include_hidden: Whether to include hidden files (starting with a dot).

    Returns:
        A list of absolute file paths.
    """

    file_paths = []

    # Walk through the directory tree starting at absolute_path
    for root, dirs, files in os.walk(absolute_path):
        
        # Skip .git and __pycache__ directories
        for skip_dir in [".git", "__pycache__"]:
            if skip_dir in dirs:
                dirs.remove(skip_dir)

        for file in files:
            # Skip files based on hidden status and .pyc extension
            if not include_hidden and file.startswith("."):
                continue
            if file.endswith(".pyc"):
                continue  # Skip compiled bytecode files

            # Add the full file path to the list
            file_paths.append(os.path.join(root, file))
    
    # Return the complete list of file paths
    return file_paths


def get_file_paths(absolute_path: str, filenames: list[str] | None, recent_only: bool) -> list[str]:
    """
    Select files to include based on recency and provided filenames.

    Args:
        absolute_path: Root directory to scan if filenames are not provided.
        filenames: Optional list of specific files to include.
        recent_only: Whether to filter for recently modified files.

    Returns:
        A list of selected file paths.
    """
    # If specific filenames are provided, filter them by recency if needed
    if filenames:
        return [f for f in filenames if not recent_only or is_recently_modified(f)]
    
    # Otherwise, list all files in the directory and filter by recency if needed
    all_files = list_all_files(absolute_path)
    selected = []

    # Filter files based on recency
    for f in all_files:
        logging.info("Checking file: %s", f)
        if not recent_only or is_recently_modified(f):
            selected.append(f)
            logging.info("Included file: %s", f)

    # Return the final list of selected files
    return selected
