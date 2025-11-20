import pytest
import tempfile
import os

from repository_context_packager.analyzer.paths import validate_paths


class TestValidatePaths:

    def test_single_directory_path(self):
        """Test with a single valid directory path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            directory, filenames = validate_paths([temp_dir])

            assert directory == temp_dir
            assert filenames == []

    def test_multiple_file_paths(self):
        """Test with multiple file paths (no directory)."""
        file_paths = ["file1.txt", "file2.py", "file3.md"]

        directory, filenames = validate_paths(file_paths)

        assert directory is None
        assert filenames == file_paths

    def test_single_file_path(self):
        """Test with a single file path."""
        file_path = "single_file.txt"

        directory, filenames = validate_paths([file_path])

        assert directory is None
        assert filenames == [file_path]
