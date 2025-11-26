"""Configuration module for VRChat Poker Agent."""

import os


def get_video_source() -> int | str | None:
    """Get the video source from environment variables.

    Returns:
        int: If the source is a digit (camera index).
        str: If the source is a string (URL or file path).
        None: If the source is not set (default behavior).
    """
    source = os.getenv("VRCHAT_VIDEO_SOURCE")
    if source is None:
        return None

    if source.isdigit():
        return int(source)

    return source
