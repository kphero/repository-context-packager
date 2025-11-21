# repository-context-packager

**Version:** 1.0.0

A command-line tool to analyze local git repositories and create a text file containing repository content optimized for sharing with Large Language Models.

---

## Features

-   Analyze one or more files or directories
-   Extract Git metadata (latest commit, author, branch)
-   Display full file structure (excluding `.git`)
-   Output contents of each file
-   Supports flexible CLI usage
-   Basic summary statistics (file count, total lines)

### Additional features:

-   **Output to File**: Output can be written to a file or displayed in terminal
-   **File Exclusion**: Automatically exclude files and directories listed in `.gitignore`
-   **Comment Removal**: Option to remove comments from code files
-   **Configuration File**: Set defaults via `.scan-repo-config.toml`

---

## Installation

### Install from PyPI (Recommended)

The easiest way to install is via pip:

```bash
pip install repository-context-packager
```

### Prerequisites

-   **Python 3.7+**
    ```bash
    python --version
    ```
-   **Git** (for Git metadata extraction)
    ```bash
    git --version
    ```

---

## Usage

After installation, you can use the tool with the `scan-repo` command:

```bash
scan-repo [paths] [options]
```

### Basic Examples

-   **Analyze current directory and display results:**

    ```bash
    scan-repo .
    ```

-   **Analyze a folder and write results to a file:**

    ```bash
    scan-repo ./my_project -o context-package.md
    ```

-   **Analyze multiple files:**

    ```bash
    scan-repo file1.txt file2.md
    ```

-   **Analyze only recently modified files:**

    ```bash
    scan-repo . --recent
    ```

-   **Remove comments from code files:**

    ```bash
    scan-repo . --remove-comments -o output.md
    ```

-   **Display help:**
    ```bash
    scan-repo --help
    ```

---

## Command-Line Arguments

| Argument              | Alias | Type     | Description                                                                    |
| --------------------- | ----- | -------- | ------------------------------------------------------------------------------ |
| `--version`           | `-v`  | Flag     | Displays tool name and version number                                          |
| `--output [filename]` | `-o`  | Optional | Write results to a file. If no filename is given, defaults to `output.txt`.    |
| `paths`               | —     | List     | One or more file or directory paths to analyze. Defaults to current directory. |
| `--recent`            | `-r`  | Flag     | Include only recently modified files (in the last 7 days)                      |
| `--verbose`           | `-vb` | Flag     | Enable verbose logging                                                         |
| `--max-file-size`     | —     | Integer  | Maximum file size in bytes to include (default: 16KB)                          |
| `--remove-comments`   | `-rc` | Flag     | Remove comments from code files in the output                                  |

---

## Configuration via TOML

You can set default options in `.scan-repo-config.toml` in your project directory:

```toml
output = "default_output.txt"
recent = false              # Include only recent files? (true/false)
verbose = false
paths = ["src"]             # can be a string or a list of paths
max_file_size = 16384       # in bytes
remove_comments = false     # Remove comments from code files?
```

CLI arguments always override values in the config file. If the file exists but is invalid TOML, the tool will exit with an error.

---

## Output Format

```markdown
# Repository Context

## File System Location

/absolute/path/to/repo/being/analyzed

## Git Info

-   Commit: <commit-sha>
-   Branch: <branch-name>
-   Author: <author-name>
-   Date: <commit-date>

## Structure

<project-structure>

## File Contents

### File: <file-name>

<file-content>

## Summary

-   Total files: <file-count>
-   Total lines: <line-count>
```

---

## Development Installation

If you want to contribute or modify the code:

### 1. Clone the Repository

```bash
git clone https://github.com/kphero/repository-context-packager.git
cd repository-context-packager
```

### 2. Install in Editable Mode

```bash
pip install -e .
```

This installs the package in "editable" mode, so changes to the source code take effect immediately.

### 3. Run Tests

```bash
pytest
```

---

## Troubleshooting

-   **Command not found after installation**: Make sure your Python Scripts directory is in your PATH, or use `python -m repository_context_packager.analyzer.cli` instead.
-   **Missing GitPython**: This should install automatically, but if not: `pip install GitPython`
-   **Permission errors**: Try using a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install repository-context-packager
    ```

---

## License

[GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html) License. See `LICENSE` file for details.

---

## Contributing

All contributions welcome—whether it's fixing bugs, improving documentation, suggesting new features, or submitting code enhancements.

Please feel free to:

-   Report bugs via [GitHub Issues](https://github.com/kphero/repository-context-packager/issues)
-   Submit pull requests
-   Suggest new features

---

## Links

-   **PyPI Package**: https://pypi.org/project/repository-context-packager/
-   **GitHub Repository**: https://github.com/kphero/repository-context-packager
-   **Issue Tracker**: https://github.com/kphero/repository-context-packager/issues

---
