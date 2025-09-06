import argparse
import datetime
from pathlib import Path

parser = argparse.ArgumentParser()
version_num = "0.1.0"

parser.add_argument(
    "-v", "--version", 
    help="Displays tool name and version number",
    action="version",
    version=f"Repository Context Packager {version_num}"
    )

args = parser.parse_args()

