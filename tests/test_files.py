import pytest
import tempfile
import os
import time
from unittest.mock import patch, MagicMock
from repository_context_packager.analyzer.files import is_recently_modified


@pytest.mark.parametrize("days_ago,threshold,expected", [
    (1, 7, True),    # 1 day ago, 7-day threshold -> recent
    (5, 7, True),    # 5 days ago, 7-day threshold -> recent
    (10, 7, False),  # 10 days ago, 7-day threshold -> not recent
    (0.5, 1, True),  # 12 hours ago, 1-day threshold -> recent
    (2, 1, False),   # 2 days ago, 1-day threshold -> not recent
    (31, 30, False),  # 31 days ago, 30-day threshold -> not recent
])
def test_various_time_thresholds(days_ago, threshold, expected):
    """Test various combinations of file age and thresholds."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test")
        temp_path = f.name

    try:
        # Mock modification time
        mod_time = time.time() - (days_ago * 24 * 60 * 60)

        with patch('os.stat') as mock_stat:
            mock_stat.return_value = MagicMock(st_mtime=mod_time)

            result = is_recently_modified(temp_path, recent_day=threshold)

            assert result == expected
    finally:
        os.unlink(temp_path)


def test_file_modified_exactly_at_threshold():
    """Test file modified exactly at the threshold boundary."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test")
        temp_path = f.name

    try:
        # Fix both timestamps to eliminate timing variance
        fixed_current_time = 1000000.0
        fixed_mod_time = fixed_current_time - (30 * 24 * 60 * 60)

        with patch('time.time', return_value=fixed_current_time):
            with patch('os.stat') as mock_stat:
                mock_stat.return_value = MagicMock(st_mtime=fixed_mod_time)

                result = is_recently_modified(temp_path, recent_day=30)
                assert result is True
    finally:
        os.unlink(temp_path)
