# repository-context-packager

**Version:** 0.1.0  
A command-line tool to analyze local git repositories and create a text file containing repository content optimized for sharing with Large Language Models.

---

## Features

-   Analyze one or more files or directories
-   Extract Git metadata (latest commit, author, branch)
-   Display full file structure (excluding `.git`)
-   Output contents of each file
-   Save results to a file or print to terminal
-   Supports flexible CLI usage

---

## Installation Guide

Follow these steps to install and run the **Repository Context Packager** on your system.

### 1. Prerequisites

Make sure you have the following installed:

-   **Python 3.6+**

    ```bash
    python --version
    ```

-   **pip** (Python package manager)

    ```bash
    pip --version
    ```

-   **Git** (for Git metadata extraction)
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

Or manually:

```bash
pip install GitPython
```

### 4. Test the Installation

```bash
python packager.py ./test-directory
```

Or display help:

```bash
python packager.py --help
```

### Troubleshooting

-   **Permission Denied**: Try running with elevated privileges or check file access rights.
-   **Missing GitPython**: Run `pip install GitPython`.
-   **Script Not Executing**: Ensure you're in the correct directory and using the right Python version.

---

## Command-Line Arguments

| Argument              | Alias | Type     | Description                                                                    |
| --------------------- | ----- | -------- | ------------------------------------------------------------------------------ |
| `--version`           | `-v`  | Flag     | Displays tool name and version number                                          |
| `--output [filename]` | `-o`  | Optional | Write results to a file. If no filename is given, defaults to `output.txt`.    |
| `paths`               | —     | List     | One or more file or directory paths to analyze. Defaults to current directory. |

---

## Usage

```bash
python repo-scan.py [-h] [-v] [-o [OUTPUT]] [paths ...]
```

### Examples

-   Analyze current directory and display results:

    ```bash
    python repo-scan.py .
    ```

-   Analyze a folder and write results to `report.txt`:

    ```bash
    python repo-scan.py -o report.txt ./my_project
    ```

-   Analyze multiple paths:
    ```bash
    python repo-scan.py ./src ./README.md
    ```

---

## Output Format

The tool generates a structured report including:

-   **File System Location**
-   **Git Info** (commit hash, branch, author, date)
-   **Directory Structure**
-   **File Contents**
-   **Summary** (number of files and number of lines)

---

## License

MIT License. See `LICENSE` file for details.

---
