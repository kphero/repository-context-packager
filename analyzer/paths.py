import os
import sys
import logging
import argparse

from analyzer import output


def normalize_path(path: str) -> str:
    """
    Convert a given path to its absolute, normalized form.

    Args:
        path: A relative or absolute file system path.

    Returns:
        A normalized absolute path string.
    """
    return os.path.normpath(os.path.abspath(path))


def validate_paths(paths: list[str]) -> tuple[str | None, list[str]]:
    """
    Validate a list of input paths and separate them into a directory or filenames.

    Rules:
        - Only one directory path is allowed.
        - Cannot mix directory and file paths in the same input.

    Args:
        paths: A list of file or directory paths provided by the user.

    Returns:
        A tuple containing:
            - The directory path (or None if only filenames are provided).
            - A list of filenames.

    Raises:
        ValueError: If more than one directory is provided or if both directory and filenames are mixed.
    """
    directories = []
    filenames = []

    # Normalize each path and classify as directory or file
    for path in paths:
        abs_path = normalize_path(path)
        if os.path.isdir(abs_path):
            directories.append(abs_path)
        else:
            filenames.append(path)

    # Enforce validation rules
    if len(directories) > 1:
        raise ValueError("Only one directory path is allowed.")
    if directories and filenames:
        raise ValueError("Please enter only a single directory path OR one or more filenames.")

    # Return the directory (or None) and the list of filenames
    return (directories[0] if directories else None, filenames)


def analyze_path_args(args: argparse.Namespace) -> None:
    """
    Entry point for path analysis logic.

    Determines whether to analyze a directory or a list of filenames based on user input.
    Validates paths, logs progress, and delegates to `output.content_output`.

    Args:
        args: Parsed CLI arguments containing:
            - paths: List of input paths (files or a single directory).
            - recent: Whether to filter by recently modified files.
            - output: Path to write the results.
            - max_file_size: Maximum number of bytes to read per file.

    Returns:
        None. Exits the program with code 1 if validation fails or files are missing.
    """
    try:
        # Separate input into either a directory or a list of filenames
        directory, filenames = validate_paths(args.paths)
    except ValueError as e:
        # Log validation error and exit
        logging.error(str(e))
        sys.exit(1)

    if directory:
        # Directory mode: analyze all files within the directory
        logging.info("Analyzing directory: %s", directory)
        output.content_output(
            directory,
            args.recent,
            None,
            args.output,
            args.max_file_size
        )

    elif filenames:
        # File mode: search for filenames in the current working directory
        search_dir = os.getcwd()
        logging.info("Searching in directory: %s", search_dir)

        # Confirm each filename exists somewhere in the directory tree
        for name in filenames:
            found = any(name in files for _, _, files in os.walk(search_dir))
            if not found:
                logging.error("%s not found.", name)
                sys.exit(1)
            logging.info("Found %s", name)

        # Analyze the matched files
        output.content_output(
            search_dir,
            args.recent,
            filenames,
            args.output,
            args.max_file_size
        )