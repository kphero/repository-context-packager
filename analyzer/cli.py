import argparse
import logging
import os
import sys

from analyzer import config, paths

VERSION_NUM = "0.2.1"
DEFAULT_MAX_FILE_BYTES = 16 * 1024


def build_parser():
    parser = argparse.ArgumentParser(
        description="Repository Context Packager - scan repo and output context"
    )
    parser.add_argument(
        "-v", "--version", 
        help="Displays tool name and version number",
        action="version",
        version=f"Repository Context Packager {VERSION_NUM}"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Directory path OR one or more filenames (default: current directory)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Write results to file instead of stdout"
    )
    parser.add_argument(
        "-r", "--recent",
        action="store_true",
        help="Include only recently modified files"
    )
    parser.add_argument(
        "-vb", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--max-file-size",
        type=int,
        default=None,
        help="Maximum file size in bytes to include (default from config or 16KB)"
    )

    return parser


def main(argv: list[str] | None = None) -> None:
    """
    Main entry point for the CLI tool.

    - Parses command-line arguments.
    - Configures logging verbosity.
    - Loads and merges configuration defaults.
    - Ensures valid input paths.
    - Delegates to core analysis logic.

    Args:
        argv: Optional list of CLI arguments.

    Returns:
        None. Exits the program with code 1 on fatal error.
    """
    # Parse CLI arguments
    parser = build_parser()
    args = parser.parse_args(argv)

    # Configure logging based on verbosity flag
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s: %(message)s"
    )

    # Load optional config file
    cfg = config.load_config_file()

    # Merge CLI args with config defaults
    args.output = config.merge_config(args, cfg, "output", str, args.output)
    args.recent = config.merge_config(args, cfg, "recent", bool, args.recent)
    args.verbose = config.merge_config(args, cfg, "verbose", bool, args.verbose)
    args.paths = config.merge_config(args, cfg, "paths", list, args.paths or [])
    args.max_file_size = config.merge_config(
        args, cfg, "max_file_size", int, args.max_file_size
    ) or DEFAULT_MAX_FILE_BYTES

    # Default to current working directory if no paths are provided
    if not args.paths:
        args.paths = [os.getcwd()]

    # Delegate to core logic
    try:
        paths.analyze_path_args(args)
    except Exception as e:
        logging.error("Fatal error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()