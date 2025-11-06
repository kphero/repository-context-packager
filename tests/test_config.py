import pytest
import tempfile
import os

from analyzer.config import load_config_file, DEFAULT_CONFIG_FILE


class TestLoadConfigFile:

    def test_config_file_not_found(self, caplog):
        """Test behavior when config file doesn't exist."""
        assert load_config_file("/nonexistent/path/config.toml") == {}
        assert "No config file found" in caplog.text

    def test_default_path(self):
        """Test with default path."""
        assert load_config_file() == load_config_file(DEFAULT_CONFIG_FILE)

    def test_empty_config_file(self):
        """Test loading an empty TOML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write('')
            temp_path = f.name

        try:
            result = load_config_file(temp_path)

            assert result == {}
        finally:
            os.unlink(temp_path)

    def test_toml_options(self, caplog):
        """Test behavior with correct TOML options."""
        content = (
            'paths = ""\n'
            'output = "context-package.md"\n'
            'recent = true\n'
            'verbose = true\n'
            'max_file_size = 16238\n'
            'remove-comments = true\n'
        )
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = load_config_file(temp_path)

            assert result is not None
            assert result["paths"] == ""
            assert result["output"] == "context-package.md"
            assert result["recent"] is True
            assert result["verbose"] is True
            assert result["max_file_size"] == 16238
            assert result["remove-comments"] is True
            assert "Loaded config from" in caplog.text
        finally:
            os.unlink(temp_path)

    def test_wrong_toml_options(self, caplog):
        """Test behavior with invalid TOML settings."""
        content = (
            'settings = true'
            'baba = "bingo"'
        )
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(content)
            temp_path = f.name

        try:
            result = load_config_file(temp_path)

            assert result == {}
            assert "Failed to load config file" in caplog.text
        finally:
            os.unlink(temp_path)
