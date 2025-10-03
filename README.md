# repository-context-packager

**Version:** 0.1.3

A command-line tool to analyze local git repositories and create a text file containing repository content optimized for sharing with Large Language Models.

---

## Features

- Analyze one or more files or directories
- Extract Git metadata (latest commit, author, branch)
- Display full file structure (excluding `.git`)
- Output contents of each file
- Supports flexible CLI usage
- Basic summary statistics (file count, total lines)

### Additional features:

- Output to File: Output can be written to a file or displayed in terminal
- File Exclusion: Automatically exclude files and directories listed in `.gitignore`

---

## Installation Guide

Follow these steps to install and run the **Repository Context Packager** on your system.

### 1. Prerequisites

Make sure you have the following installed:

- **Python 3.6+**

  ```bash
  python --version
  ```

- **pip** (Python package manager)

  ```bash
  pip --version
  ```

- **Git** (for Git metadata extraction)
  ```bash
  git --version
  ```

### 2. Clone the Repository

```bash
git clone https://github.com/kphero/repository-context-packager.git
cd repo-context-packager
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test the Installation

```bash
python repo-scan.py ./test-directory
```

Or display help:

```bash
python repo-scan.py --help
```

### Troubleshooting

- **Permission Denied**: Try running with elevated privileges or check file access rights.
- **Missing GitPython**: Run `pip install GitPython`.
- **Script Not Executing**: Ensure you're in the correct directory and using the right Python version.

---

## Command-Line Arguments

| Argument              | Alias | Type     | Description                                                                    |
| --------------------- | ----- | -------- | ------------------------------------------------------------------------------ |
| `--version`           | `-v`  | Flag     | Displays tool name and version number                                          |
| `--output [filename]` | `-o`  | Optional | Write results to a file. If no filename is given, defaults to `output.txt`.    |
| `paths`               | —     | List     | One or more file or directory paths to analyze. Defaults to current directory. |
| `--recent`            | `-r`  | Flag     | Include only recently modified files (in the last 7 days)                      |

---

### Configuration via TOML

You can also set default options in `.repo-scan-config.toml`. Example:

```toml
output = "default_output.txt"
recent = false        # Include only recent files? (true/false)
verbose = false
paths = ["src"]        # can be a string or a list of paths
max_file_size = 16384  # in bytes
```
CLI arguments always override values in the config file. If the file exists but is invalid TOML, the tool will exit with an error.

---

## Usage

```bash
python repo-scan.py [-h] [-v] [-r] [paths ...] [-o [OUTPUT]]
```

### Examples

- Analyze current directory and display results:

  ```bash
  python repo-scan.py .
  ```

- Analyze a folder and write results to `context-package.md`:

  ```bash
  python repo-scan.py ./my_project -o context-package.md
  ```

- Analyze multiple files:

  ```bash
  python repo-scan.py file1.txt file2.md
  ```

- Analyze recent files in current directory:

  ```bash
  python repo-scan.py . -r
  ```

  > **Note:** `repo-scan.py` only detects files located in the same directory as the script. Ensure that all target files are placed in the script’s directory before execution, or that `repo-scan.py` is placed in the directory where the files are located.

---

## Output Format

```
# Repository Context

## File System Location

/absolute/path/to/repo/being/analyzed

## Git Info

- Commit: <commit-sha>
- Branch: <branch-name>
- Author: <author-name>
- Date: <commit-date>

## Structure
<project-structure>

## File Contents

### File: <file-name>
<file-content>

## Summary
- Total files: <file-count>
- Total lines: <line-count>
```

---

## License

MIT License. See `LICENSE` file for details.

---

## Contributing

All contributions welcome—whether it's fixing bugs, improving documentation, suggesting new features, or submitting code enhancements.

---
