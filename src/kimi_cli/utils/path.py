import asyncio
import os
import re
from pathlib import Path

import aiofiles.os


async def next_available_rotation(path: Path) -> Path | None:
    """
    Find the next available rotation path for a given path using atomic file creation.

    This function handles race conditions by using atomic operations (O_CREAT|O_EXCL for files,
    mkdir for directories) with automatic retry on conflicts.

    Args:
        path: The base path for which to find the next available rotation.

    Returns:
        Path to the next available rotation file/directory, or None if parent doesn't exist.

    Raises:
        RuntimeError: If unable to create a rotation after maximum retry attempts.
    """
    if not path.parent.exists():
        return None

    base_name = path.stem
    suffix = path.suffix
    pattern = re.compile(rf"^{re.escape(base_name)}_(\d+){re.escape(suffix)}$")

    # Maximum number of retry attempts to handle race conditions
    max_attempts = 100

    for _attempt in range(max_attempts):
        # Scan directory to find current maximum rotation number
        max_num = 0
        for p in await aiofiles.os.listdir(path.parent):
            if m := pattern.match(p):
                max_num = max(max_num, int(m.group(1)))

        # Try to create the next rotation atomically
        next_num = max_num + 1
        next_path = path.parent / f"{base_name}_{next_num}{suffix}"

        try:
            # Use atomic operations to create the file/directory
            await _atomic_create(next_path)
            return next_path
        except FileExistsError:
            # Another process created this file/directory, retry with updated scan
            continue

    # If we exhausted all attempts, raise an error
    raise RuntimeError(
        f"Failed to create rotation for {path} after {max_attempts} attempts. "
        "This may indicate excessive concurrent access."
    )


async def _atomic_create(path: Path) -> None:
    """
    Atomically create a file or directory at the given path.

    For files (paths with extensions), uses os.open with O_CREAT|O_EXCL flags.
    For directories (paths without extensions or existing as directories), uses os.mkdir.

    Args:
        path: The path to create atomically.

    Raises:
        FileExistsError: If the path already exists.
    """

    def _create_sync() -> None:
        """Synchronous helper for atomic creation."""
        # Check if this should be a directory or file
        # If suffix is empty or if siblings suggest it's a directory pattern
        if path.suffix == "":
            # No extension, treat as directory
            os.mkdir(path)
        else:
            # Has extension, treat as file
            # Use O_CREAT|O_EXCL for atomic file creation
            # O_CREAT: Create file if it doesn't exist
            # O_EXCL: Fail if file already exists (atomic check-and-create)
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            os.close(fd)

    # Run the blocking operation in a thread pool to maintain async compatibility
    await asyncio.to_thread(_create_sync)
