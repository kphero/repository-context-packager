import io
import os
import time
import logging

from analyzer import git, structure, files

def content_output(absolute_path, contain_recent_files_only,
                   filenames=None, output=None, max_file_size=16*1024, remove_comments=False) -> None:
    """
    Generate repository context output for a directory or set of files.
    """
    buffer = io.StringIO()
    file_count = 0
    line_count = 0

    logging.info("Starting content output for path: %s", absolute_path)

    # Repository context header
    buffer.write("# Repository Context\n\n")
    buffer.write("## File System Location\n\n")
    buffer.write(f"{absolute_path}\n\n")

    # Git info
    buffer.write("## Git Info\n\n")
    git_info = git.pull_git_info(absolute_path)
    if git_info:
        for k, v in git_info.items():
            buffer.write(f"- {k.capitalize()}: {v}\n")
        buffer.write("\n")
    else:
        buffer.write("Not a git repository\n\n")

    # Structure
    buffer.write("## Structure\n```\n")
    structure_str = structure.analyze_structure(absolute_path)
    buffer.write(f"{structure_str}\n```\n\n")

    # File contents
    buffer.write("## File Contents\n")
    if contain_recent_files_only:
        buffer.write("[Only the recently modified files are included]\n\n")
        logging.info("Filtering for recently modified files only.")
    else:
        buffer.write("\n")
        logging.info("Including all files.")

    file_paths = files.get_file_paths(absolute_path, filenames, contain_recent_files_only)

    if not file_paths:
        buffer.write("No file content available.\n\n")
        logging.info("No files matched the criteria.")
    else:
        for file_path in file_paths:
            section, lines = render_file_section(file_path, contain_recent_files_only, max_file_size, remove_comments)
            buffer.write(section)
            file_count += 1
            line_count += lines

    # Summary
    buffer.write("## Summary\n")
    if contain_recent_files_only:
        buffer.write(f"- Total files (recently changed): {len(file_paths)}\n")
    else:
        buffer.write(f"- Total files: {file_count}\n")
    buffer.write(f"- Total lines: {line_count}\n\n")

    # Output
    content = buffer.getvalue()

    if output:
        logging.info("Writing results to file: %s", output)
        write_results(content, output)
    else:
        logging.info("Displaying results to terminal.")
        print("Displaying results..\n")
        print(content)

def render_file_section(file_path: str, recent_only: bool, max_file_size: int, remove_comments: bool) -> tuple[str, int]:
    """
    Render a markdown-formatted section for a file, including optional modification time.

    Args:
        file_path: Path to the file.
        recent_only: Whether to include modification time.
        max_file_size: Maximum number of bytes to read from the file.

    Returns:
        A tuple containing:
            - Markdown-formatted string for the file section.
            - Number of lines in the file.
    """
    # Create the section header with filename
    filename = os.path.basename(file_path)
    header = f"### File: {filename}"
    
    # Append modification time if recent_only is enabled
    if recent_only:
        try:
            # Get the last modification time
            ts = os.path.getmtime(file_path)
            modified = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        except Exception as e:
            logging.error("Could not retrieve modification time for %s: %s", file_path, e)
            modified = "Unknown"
        
        # Append modification time to header
        header += f" (Modified: {modified})"
    
    # Analyze file content
    content, lines = files.analyze_file_content(file_path, max_file_size, remove_comments)

    # Format the section with markdown code block
    return f"{header}\n```\n{content}\n```\n\n", lines


def write_results(content: str, output: str) -> None:
    """
    Write the given content to a file at the specified path.

    Args:
        content: The string content to write.
        output: The path to the output file.

    Returns:
        None
    """
    try:
        # Open the file in write mode with UTF-8 encoding
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)

        # Log success message
        logging.info("Results successfully written to %s", output)

    except Exception as e:
        # Log error if writing fails
        logging.error("Failed to write to %s: %s", output, e)