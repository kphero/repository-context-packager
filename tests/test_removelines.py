import pytest
from repository_context_packager.analyzer.removelines import remove_hash_comments


class TestRemoveHashComments:

    def test_empty_string(self):
        """Test with empty input."""
        assert remove_hash_comments("") == ""

    def test_no_comments(self):
        """Test code without any comments."""
        code = "x = 5\ny = 10\nprint(x + y)"
        assert remove_hash_comments(code) == code

    def test_single_hash_comment_line(self):
        """Test removal of a single line with only a hash comment."""
        code = "# This is a comment"
        assert remove_hash_comments(code) == ""

    def test_multiple_hash_comment_lines(self):
        """Test removal of multiple hash comment lines."""
        code = "# Comment 1\n# Comment 2\n# Comment 3"
        assert remove_hash_comments(code) == ""

    def test_hash_comment_with_leading_whitespace(self):
        """Test removal of hash comments with leading whitespace."""
        code = "    # Indented comment\n\t# Tab indented comment"
        assert remove_hash_comments(code) == ""

    # def test_inline_hash_comment(self):
    #     """Test removal of inline hash comments."""
    #     code = 'x = 5  # This is an inline comment'
    #     expected = 'x = 5'
    #     assert remove_hash_comments(code) == expected

    def test_hash_in_string(self):
        """Test that hash symbols inside strings are preserved."""
        code = 'text = "This # is not a comment"'
        assert remove_hash_comments(code) == code

    def test_single_line_docstring_double_quotes(self):
        """Test removal of single-line docstring with double quotes."""
        code = '"""This is a single-line docstring"""'
        assert remove_hash_comments(code) == ""

    def test_single_line_docstring_single_quotes(self):
        """Test removal of single-line docstring with single quotes."""
        code = "'''This is a single-line docstring'''"
        assert remove_hash_comments(code) == ""

    def test_multiline_docstring_double_quotes(self):
        """Test removal of multi-line docstring with double quotes."""
        code = '"""\nThis is a\nmulti-line docstring\n"""'
        assert remove_hash_comments(code) == ""

    def test_multiline_docstring_single_quotes(self):
        """Test removal of multi-line docstring with single quotes."""
        code = "'''\nThis is a\nmulti-line docstring\n'''"
        assert remove_hash_comments(code) == ""

    def test_function_with_docstring(self):
        """Test removal of docstring from a function."""
        code = (
            'def foo():\n'
            '    """Function docstring"""\n'
            '    return 42'
        )
        expected = (
            'def foo():\n'
            '    return 42'
        )

        assert remove_hash_comments(code) == expected

    def test_function_with_multiline_docstring(self):
        """Test removal of multi-line docstring from a function."""
        code = (
            'def bar():\n'
            '    """\n'
            '    Multi-line\n'
            '    docstring\n'
            '    """\n'
            '    x = 10\n'
            '    return x'
        )
        expected = (
            'def bar():\n'
            '    x = 10\n'
            '    return x'
        )

        assert remove_hash_comments(code) == expected

    def test_mixed_comments_and_code(self):
        """Test code with both hash comments and actual code."""
        code = (
            '# Header comment\n'
            'x = 5\n'
            '# Another comment\n'
            'y = 10\n'
            'z = x + y'
        )
        expected = (
            'x = 5\n'
            'y = 10\n'
            'z = x + y'
        )

        assert remove_hash_comments(code) == expected

    def test_class_with_docstring_and_comments(self):
        """Test class with both docstring and hash comments."""
        code = (
            'class MyClass:\n'
            '    """Class docstring"""\n'
            '    # This is a comment\n'
            '    def __init__(self):\n'
            '        self.x = 5'
        )
        expected = (
            'class MyClass:\n'
            '    def __init__(self):\n'
            '        self.x = 5'
        )

        assert remove_hash_comments(code) == expected
