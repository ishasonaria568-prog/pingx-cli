"""
PING — Lightweight Standalone Network Diagnostics CLI Tool
===========================================================
A clean, minimal, standalone ICMP ping utility for Kali Linux and UNIX systems.

Author: Isha Sonaria
GitHub: https://github.com/ishasonaria568-prog
License: MIT
"""

__tool_name__ = "PING"
__executable__ = "pingx"
__version__ = "1.0.0"
__author__ = "Isha Sonaria"
__github__ = "https://github.com/ishasonaria568-prog"

from .cli import main
from .icmp import ICMPPing, PingPacketResult
from .statistics import PingStatistics

__all__ = [
    "__tool_name__",
    "__executable__",
    "__version__",
    "__author__",
    "__github__",
    "main",
    "ICMPPing",
    "PingPacketResult",
    "PingStatistics",
]
