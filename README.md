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

## Installation

Make sure you have Python 3 installed and the `GitPython` library:

```bash
pip install gitpython
```

## Usages

```
python pack-repo.py [paths] [-o OUTPUT]
```

### Example

```
# Analyze the current directory and print results
python pack-repo.py .

# Analyze a specific project folder and write to a file
python pack-repo.py /path/to/project -o context.txt

# Analyze multiple files
python pack-repo.py src/main.py src/utils.py

# Display version info
python pack-repo.py --version
```
