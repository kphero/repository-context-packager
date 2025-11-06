import pytest
import tempfile
import os
import time
from unittest.mock import patch, MagicMock
from analyzer.files import is_recently_modified


@pytest.mark.parametrize("days_ago,threshold,expected", [
    (1, 7, True),    # 1 day ago, 7-day threshold -> recent
    (5, 7, True),    # 5 days ago, 7-day threshold -> recent
    (10, 7, False),  # 10 days ago, 7-day threshold -> not recent
    (0.5, 1, True),  # 12 hours ago, 1-day threshold -> recent
    (2, 1, False),   # 2 days ago, 1-day threshold -> not recent
    (30, 30, True),  # 30 days ago, 30-day threshold -> recent
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
