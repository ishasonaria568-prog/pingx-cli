"""
PING — Lightweight Standalone Network Diagnostics CLI Tool
Utility functions, input validation, and minimal terminal styling.
Author: Isha Sonaria (https://github.com/ishasonaria568-prog)
"""

import os
import re
import sys
import ipaddress
from typing import Tuple


class Colors:
    """Minimal ANSI color codes for terminal formatting."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"


_COLOR_ENABLED = True


def set_color_enabled(enabled: bool) -> None:
    """Explicitly enable or disable colored terminal output."""
    global _COLOR_ENABLED
    _COLOR_ENABLED = enabled


def is_color_enabled() -> bool:
    """Check if color is enabled (respects NO_COLOR env var and stdout isatty)."""
    global _COLOR_ENABLED
    if not _COLOR_ENABLED:
        return False
    if "NO_COLOR" in os.environ:
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    return sys.stdout.isatty() or os.environ.get("FORCE_COLOR") == "1"


def colorize(text: str, color_code: str) -> str:
    """Wrap text in ANSI color codes if enabled."""
    if is_color_enabled():
        return f"{color_code}{text}{Colors.RESET}"
    return text


def green(text: str) -> str:
    return colorize(text, Colors.GREEN)


def red(text: str) -> str:
    return colorize(text, Colors.RED)


def yellow(text: str) -> str:
    return colorize(text, Colors.YELLOW)


def cyan(text: str) -> str:
    return colorize(text, Colors.CYAN)


def bold(text: str) -> str:
    return colorize(text, Colors.BOLD)


def dim(text: str) -> str:
    return colorize(text, Colors.DIM)


def get_version_info() -> str:
    """Return concise version and developer branding info."""
    c_bold = Colors.BOLD if is_color_enabled() else ""
    c_cyan = Colors.CYAN if is_color_enabled() else ""
    c_reset = Colors.RESET if is_color_enabled() else ""
    return (
        f"{c_bold}PING v1.0.0{c_reset} ({c_cyan}pingx{c_reset})\n"
        "Lightweight Standalone Network Diagnostic Utility\n"
        "Built by Isha Sonaria\n"
        "GitHub: https://github.com/ishasonaria568-prog\n"
        "Platform priority: Kali Linux | MIT License"
    )


def sanitize_target(target: str) -> str:
    """
    Clean and normalize user-provided target string.
    Removes protocols (http://, https://) and trailing paths.
    """
    cleaned = target.strip()
    if cleaned.startswith("http://"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("https://"):
        cleaned = cleaned[8:]
    cleaned = cleaned.split("/")[0]
    if ":" in cleaned and not (cleaned.startswith("[") and "]" in cleaned) and cleaned.count(":") == 1:
        cleaned = cleaned.split(":")[0]
    elif cleaned.startswith("[") and "]" in cleaned:
        cleaned = cleaned.strip("[]")
    return cleaned


def is_valid_ipv4(ip: str) -> bool:
    """Check if string is a valid IPv4 address."""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except (ipaddress.AddressValueError, ValueError):
        return False


def is_valid_ipv6(ip: str) -> bool:
    """Check if string is a valid IPv6 address."""
    try:
        ipaddress.IPv6Address(ip)
        return True
    except (ipaddress.AddressValueError, ValueError):
        return False


_HOSTNAME_REGEX = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
)


def is_valid_hostname(hostname: str) -> bool:
    """Check if string is a valid RFC 1123 DNS hostname."""
    if not hostname or len(hostname) > 253:
        return False
    if hostname == "localhost":
        return True
    return bool(_HOSTNAME_REGEX.match(hostname))


def validate_target(target: str) -> Tuple[str, str]:
    """
    Validate target and determine its address family type.
    Returns (cleaned_target, target_type) where target_type is 'ipv4', 'ipv6', or 'hostname'.
    Raises ValueError if target is invalid.
    """
    if not target or not isinstance(target, str):
        raise ValueError("Target host or IP address cannot be empty.")

    cleaned = sanitize_target(target)
    if not cleaned:
        raise ValueError("Invalid target format.")

    # Strictly reject shell metacharacters
    forbidden = [";", "&", "|", "`", "$", "(", ")", "<", ">", "\n", "\r", " ", "\t", "\\"]
    for ch in forbidden:
        if ch in cleaned:
            raise ValueError(f"Illegal character '{ch}' in target. Input rejected.")

    if is_valid_ipv4(cleaned):
        return cleaned, "ipv4"
    if is_valid_ipv6(cleaned):
        return cleaned, "ipv6"
    if is_valid_hostname(cleaned):
        return cleaned, "hostname"

    raise ValueError(f"'{target}' is neither a valid IPv4/IPv6 address nor a valid hostname.")


def format_ms(val: float) -> str:
    """Format milliseconds value to 2 decimal places."""
    return f"{val:.2f} ms"
