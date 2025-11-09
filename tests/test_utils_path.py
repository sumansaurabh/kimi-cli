"""Tests for path utility functions."""

import asyncio
from pathlib import Path

import pytest

from kimi_cli.utils.path import next_available_rotation


@pytest.mark.asyncio
async def test_next_available_rotation_empty_dir(tmp_path):
    """Test next_available_rotation with empty directory."""
    test_file = tmp_path / "test.txt"
    result = await next_available_rotation(test_file)

    assert result == tmp_path / "test_1.txt"


@pytest.mark.asyncio
async def test_next_available_rotation_no_existing_rotations(tmp_path):
    """Test next_available_rotation with no existing rotation files."""
    # Create the parent directory
    test_file = tmp_path / "test.txt"

    result = await next_available_rotation(test_file)

    assert result == tmp_path / "test_1.txt"


@pytest.mark.asyncio
async def test_next_available_rotation_with_existing_rotations(tmp_path):
    """Test next_available_rotation with existing rotation files."""
    # Create existing rotation files
    (tmp_path / "test_1.txt").write_text("content1")
    (tmp_path / "test_2.txt").write_text("content2")
    (tmp_path / "test_5.txt").write_text("content5")  # Gap in numbering

    test_file = tmp_path / "test.txt"
    result = await next_available_rotation(test_file)

    # Should find the highest number (5) and return next (6)
    assert result == tmp_path / "test_6.txt"


@pytest.mark.asyncio
async def test_next_available_rotation_mixed_files(tmp_path):
    """Test next_available_rotation with mixed files in directory."""
    # Create various files, only some match the pattern
    (tmp_path / "test_1.txt").write_text("content1")
    (tmp_path / "test_3.txt").write_text("content3")
    (tmp_path / "other_file.txt").write_text("other")
    (tmp_path / "test_backup.txt").write_text("backup")
    (tmp_path / "different_2.txt").write_text("different")

    test_file = tmp_path / "test.txt"
    result = await next_available_rotation(test_file)

    # Should find the highest matching number (3) and return next (4)
    assert result == tmp_path / "test_4.txt"


@pytest.mark.asyncio
async def test_next_available_rotation_different_extensions(tmp_path):
    """Test next_available_rotation with different file extensions."""
    # Create files with same base name but different extensions
    (tmp_path / "document_1.pdf").write_text("pdf1")
    (tmp_path / "document_2.pdf").write_text("pdf2")
    (tmp_path / "document.txt").write_text("txt")  # Different extension

    test_file = tmp_path / "document.pdf"
    result = await next_available_rotation(test_file)

    # Should only consider .pdf files
    assert result == tmp_path / "document_3.pdf"


@pytest.mark.asyncio
async def test_next_available_rotation_complex_name(tmp_path):
    """Test next_available_rotation with complex file names."""
    # Note: path.stem for "my-backup_file.tar.gz" is "my-backup_file.tar"
    # and path.suffix is ".gz", so the function looks for "my-backup_file.tar_N.gz"
    (tmp_path / "my-backup_file.tar_1.gz").write_text("backup1")
    (tmp_path / "my-backup_file.tar_3.gz").write_text("backup3")

    test_file = tmp_path / "my-backup_file.tar.gz"
    result = await next_available_rotation(test_file)

    # Should find the highest number (3) and return next (4)
    assert result == tmp_path / "my-backup_file.tar_4.gz"


@pytest.mark.asyncio
async def test_next_available_rotation_parent_not_exists():
    """Test next_available_rotation when parent directory doesn't exist."""
    test_file = Path("/non/existent/directory/test.txt")
    result = await next_available_rotation(test_file)

    assert result is None


@pytest.mark.asyncio
async def test_next_available_rotation_zero_padding(tmp_path):
    """Test next_available_rotation matches zero-padded numbers (regex \\d+ matches them)."""
    # Create files with zero-padded numbers (they will match \d+ pattern)
    (tmp_path / "test_01.txt").write_text("padded1")
    (tmp_path / "test_007.txt").write_text("padded7")
    (tmp_path / "test_5.txt").write_text("normal5")

    test_file = tmp_path / "test.txt"
    result = await next_available_rotation(test_file)

    # Should find the highest number (7 from test_007.txt) and return next (8)
    assert result == tmp_path / "test_8.txt"


@pytest.mark.asyncio
async def test_next_available_rotation_large_numbers(tmp_path):
    """Test next_available_rotation with large numbers."""
    # Create files with large numbers
    (tmp_path / "log_999.txt").write_text("log999")
    (tmp_path / "log_1000.txt").write_text("log1000")
    (tmp_path / "log_1500.txt").write_text("log1500")

    test_file = tmp_path / "log.txt"
    result = await next_available_rotation(test_file)

    # Should find the highest number (1500) and return next (1501)
    assert result == tmp_path / "log_1501.txt"


@pytest.mark.asyncio
async def test_next_available_rotation_directory_with_suffix(tmp_path):
    """Test next_available_rotation with directories that have suffix-like names."""
    # Create directories with numbered suffixes
    (tmp_path / "backup_1").mkdir()
    (tmp_path / "backup_2").mkdir()
    (tmp_path / "backup_5").mkdir()

    test_dir = tmp_path / "backup"
    result = await next_available_rotation(test_dir)

    # Should find the highest number (5) and return next (6)
    assert result == tmp_path / "backup_6"


@pytest.mark.asyncio
async def test_next_available_rotation_directory_empty_suffix(tmp_path):
    """Test next_available_rotation with directories (empty suffix)."""
    # Create directories with numbered suffixes
    (tmp_path / "data_1").mkdir()
    (tmp_path / "data_3").mkdir()

    test_dir = tmp_path / "data"
    result = await next_available_rotation(test_dir)

    # Should find the highest number (3) and return next (4)
    assert result == tmp_path / "data_4"


@pytest.mark.asyncio
async def test_next_available_rotation_directory_with_extension(tmp_path):
    """Test next_available_rotation with directory names containing dots."""
    # Note: for path "config.backup", stem is "config" and suffix is ".backup"
    # So the function looks for "config_N.backup" pattern
    (tmp_path / "config_1.backup").mkdir()
    (tmp_path / "config_2.backup").mkdir()

    test_dir = tmp_path / "config.backup"
    result = await next_available_rotation(test_dir)

    # Should find the highest number (2) and return next (3)
    assert result == tmp_path / "config_3.backup"


@pytest.mark.asyncio
async def test_next_available_rotation_mixed_files_and_dirs(tmp_path):
    """Test next_available_rotation with mixed files and directories."""
    # Create both files and directories with matching patterns
    (tmp_path / "archive_1.txt").write_text("file1")
    (tmp_path / "archive_2").mkdir()  # Directory, no extension
    (tmp_path / "archive_3.txt").write_text("file3")

    test_path = tmp_path / "archive.txt"
    result = await next_available_rotation(test_path)

    # Should only consider files with matching extension (.txt)
    assert result == tmp_path / "archive_4.txt"


@pytest.mark.asyncio
async def test_next_available_rotation_directory_pattern_with_extension(tmp_path):
    """Test next_available_rotation with directory that has extension-like suffix."""
    # Note: for path "my.data", stem is "my" and suffix is ".data"
    # So the function looks for "my_N.data" pattern
    (tmp_path / "my_1.data").mkdir()
    (tmp_path / "my_2.data").mkdir()
    (tmp_path / "my_3.data").mkdir()

    test_dir = tmp_path / "my.data"
    result = await next_available_rotation(test_dir)

    # Should find the highest number (3) and return next (4)
    assert result == tmp_path / "my_4.data"


@pytest.mark.asyncio
async def test_next_available_rotation_race_condition_files(tmp_path):
    """Test next_available_rotation handles race conditions with concurrent file creation."""
    # Create some existing rotation files
    (tmp_path / "log_1.txt").write_text("log1")
    (tmp_path / "log_2.txt").write_text("log2")

    test_file = tmp_path / "log.txt"

    # Simulate concurrent calls to next_available_rotation
    async def create_rotation():
        return await next_available_rotation(test_file)

    # Run multiple concurrent rotation attempts
    results = await asyncio.gather(*[create_rotation() for _ in range(10)])

    # All results should be unique paths
    assert len(results) == len(set(results)), "All rotation paths should be unique"

    # All created files should exist
    for result in results:
        assert result.exists(), f"File {result} should exist"

    # Verify the files are numbered sequentially starting from 3
    expected_numbers = set(range(3, 13))  # 3 through 12
    actual_numbers = {int(r.stem.split("_")[1]) for r in results}
    assert actual_numbers == expected_numbers, "Files should be numbered 3-12"


@pytest.mark.asyncio
async def test_next_available_rotation_race_condition_directories(tmp_path):
    """Test next_available_rotation handles race conditions with concurrent directory creation."""
    # Create some existing rotation directories
    (tmp_path / "backup_1").mkdir()
    (tmp_path / "backup_2").mkdir()

    test_dir = tmp_path / "backup"

    # Simulate concurrent calls to next_available_rotation
    async def create_rotation():
        return await next_available_rotation(test_dir)

    # Run multiple concurrent rotation attempts
    results = await asyncio.gather(*[create_rotation() for _ in range(10)])

    # All results should be unique paths
    assert len(results) == len(set(results)), "All rotation paths should be unique"

    # All created directories should exist
    for result in results:
        assert result.exists(), f"Directory {result} should exist"
        assert result.is_dir(), f"{result} should be a directory"

    # Verify the directories are numbered sequentially starting from 3
    expected_numbers = set(range(3, 13))  # 3 through 12
    actual_numbers = {int(r.name.split("_")[1]) for r in results}
    assert actual_numbers == expected_numbers, "Directories should be numbered 3-12"


@pytest.mark.asyncio
async def test_next_available_rotation_atomic_creation_file(tmp_path):
    """Test that file creation is atomic and doesn't overwrite existing files."""
    test_file = tmp_path / "data.txt"

    # Create first rotation
    result1 = await next_available_rotation(test_file)
    assert result1 == tmp_path / "data_1.txt"
    assert result1.exists()

    # Write some content to verify it's not overwritten
    result1.write_text("important data")

    # Create second rotation
    result2 = await next_available_rotation(test_file)
    assert result2 == tmp_path / "data_2.txt"
    assert result2.exists()

    # Verify first file wasn't modified
    assert result1.read_text() == "important data"


@pytest.mark.asyncio
async def test_next_available_rotation_atomic_creation_directory(tmp_path):
    """Test that directory creation is atomic and doesn't affect existing directories."""
    test_dir = tmp_path / "cache"

    # Create first rotation
    result1 = await next_available_rotation(test_dir)
    assert result1 == tmp_path / "cache_1"
    assert result1.exists()
    assert result1.is_dir()

    # Create a file inside to verify it's not affected
    (result1 / "marker.txt").write_text("marker")

    # Create second rotation
    result2 = await next_available_rotation(test_dir)
    assert result2 == tmp_path / "cache_2"
    assert result2.exists()
    assert result2.is_dir()

    # Verify first directory wasn't modified
    assert (result1 / "marker.txt").exists()
    assert (result1 / "marker.txt").read_text() == "marker"


@pytest.mark.asyncio
async def test_next_available_rotation_high_concurrency(tmp_path):
    """Test next_available_rotation with high concurrency (stress test)."""
    test_file = tmp_path / "concurrent.log"

    # Simulate high concurrent load
    async def create_rotation():
        return await next_available_rotation(test_file)

    # Run 50 concurrent rotation attempts
    results = await asyncio.gather(*[create_rotation() for _ in range(50)])

    # All results should be unique
    assert len(results) == len(set(results)), "All rotation paths should be unique"

    # All files should exist
    for result in results:
        assert result.exists(), f"File {result} should exist"

    # Verify sequential numbering
    expected_numbers = set(range(1, 51))
    actual_numbers = {int(r.stem.split("_")[1]) for r in results}
    assert actual_numbers == expected_numbers, "Files should be numbered 1-50"


@pytest.mark.asyncio
async def test_next_available_rotation_with_gaps_concurrent(tmp_path):
    """Test concurrent rotation with existing gaps in numbering."""
    # Create files with gaps
    (tmp_path / "file_1.txt").write_text("1")
    (tmp_path / "file_5.txt").write_text("5")
    (tmp_path / "file_10.txt").write_text("10")

    test_file = tmp_path / "file.txt"

    # Run concurrent rotations
    async def create_rotation():
        return await next_available_rotation(test_file)

    results = await asyncio.gather(*[create_rotation() for _ in range(5)])

    # All results should be unique and start from 11 (max_num + 1)
    assert len(results) == len(set(results))
    expected_numbers = set(range(11, 16))
    actual_numbers = {int(r.stem.split("_")[1]) for r in results}
    assert actual_numbers == expected_numbers
