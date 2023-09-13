"""Utility functions for ytdl_img_extractor."""

import subprocess


class InvalidFPSValueError(ValueError):
    """Custom exception for invalid fps value."""

    message = "Argument must be a positive integer value"


def is_ffmpeg_installed() -> bool:
    """Check if ffmpeg is installed."""
    try:
        # Get ffmpeg version info
        # stdout and stderr prevent the output from being printed
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)  # noqa: S603, S607
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False
    return True


def check_value(arg: str) -> int:
    """Check fps value.

    Raises:
        InvalidFPSValueError: if value is not a positive integer
    """
    num = int(arg)
    if num <= 0:
        raise InvalidFPSValueError
    return num


def restrict_to_ascii(title: str) -> str:
    """Restrict the title to ASCII characters and replace spaces with underscores."""
    return "".join(char if char.isascii() and char != " " else "_" for char in title)
