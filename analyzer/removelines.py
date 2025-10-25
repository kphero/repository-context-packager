import re

def remove_comments_from_code(code: str, file_extension: str) -> str:
    """
    Remove comments (and docstrings for Python) from code based on file extension.
    Removes resulting empty lines for clean output.

    Args:
        code: The code string from which to remove comments.
        file_extension: The file extension indicating the programming language.
    
    Returns:
        Code with comments removed and empty lines collapsed.
    """
    
    if file_extension == '.py':
        code = remove_hash_comments(code)
    elif file_extension in ['.js', '.java', '.c', '.cpp']:
        code = remove_slash_comments(code)
    elif file_extension == '.html':
        code = re.sub(r'<!--.*?-->', '', code, flags=re.DOTALL)
    
    # Remove blank lines
    # code = re.sub(r'\n\s*\n+', '\n', code)
    
    return code.strip()


def remove_hash_comments(code: str) -> str:
    """Remove Python comments (#) and docstrings while preserving code."""
    lines = code.split('\n')
    result = []
    docstring = None
    
    for line in lines:
        stripped = line.lstrip() # Remove leading whitespace for checks
        
        # Skip # comment-only lines
        if stripped.startswith('#'):
            continue
        
        # If already in docstring, look for the closing quotation mark
        if docstring:
            if docstring in line:
                docstring = None
            continue

        # If line starts a docstring
        if stripped.startswith('"""') or stripped.startswith("'''"):
            quote = '"""' if stripped.startswith('"""') else "'''"
            # Check if docstring closes on same line
            if stripped.count(quote) >= 2:
                continue  # Single-line docstring, skip it
            else:
                docstring = quote 
                continue

        result.append(line)

    return '\n'.join(result)


def remove_slash_comments(code: str) -> str:
    """Remove C-style comment-only lines and multi-line comments."""
    lines = code.split('\n')
    result = []
    docstring = None
    
    for line in lines:
        stripped = line.lstrip()  # Remove leading whitespace for checks
        
        # Skip // comment-only lines
        if stripped.startswith('//'):
            continue

        # If already in docstring, look for the closing quotation mark
        if docstring:
            if docstring in line:
                docstring = None
            continue

        # If line starts a docstring
        if stripped.startswith('/*'):
            quote = '*/'
            # Check if docstring closes on same line
            if quote in line:
                continue  # Single-line docstring, skip it
            else:
                docstring = quote 
                continue
        
        result.append(line)
    
    return '\n'.join(result)