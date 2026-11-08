"""
PING — Lightweight Standalone Network Diagnostics CLI Tool
Command-line interface (CLI) entry point for the 'pingx' executable.
Author: Isha Sonaria (https://github.com/ishasonaria568-prog)
"""

import sys
import argparse
import signal
from typing import Optional, List

from . import __version__, __author__, __github__, __tool_name__, __executable__
from .utils import (
    get_version_info,
    set_color_enabled,
    red,
    bold,
    dim,
)
from .icmp import ICMPPing


def build_parser() -> argparse.ArgumentParser:
    """Build the clean Linux-style command line parser for pingx."""
    parser = argparse.ArgumentParser(
        prog="pingx",
        description="PING — Lightweight Standalone Network Diagnostic CLI Tool by Isha Sonaria.",
        epilog="GitHub: https://github.com/ishasonaria568-prog | Built for Kali Linux",
        add_help=True,
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=None,
        help="Destination hostname or IP address to ping (e.g., google.com, 127.0.0.1)",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=4,
        help="Stop after sending COUNT packets (default: 4, 0 for continuous)",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=1.0,
        help="Wait INTERVAL seconds between sending each packet (default: 1.0, min: 0.2)",
    )
    parser.add_argument(
        "-W",
        "--timeout",
        type=float,
        default=2.0,
        help="Time to wait for a response, in seconds (default: 2.0)",
    )
    parser.add_argument(
        "-4",
        dest="ipv4",
        action="store_true",
        help="Force IPv4 transport only",
    )
    parser.add_argument(
        "-6",
        dest="ipv6",
        action="store_true",
        help="Force IPv6 transport only",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI terminal colors",
    )
    parser.add_argument(
        "-V",
        "-v",
        "--version",
        dest="show_version",
        action="store_true",
        help="Show version and developer branding",
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI execution flow."""
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()

    # Handle quick flags or empty invocation
    if not argv:
        parser.print_help()
        return 0

    # Handle standalone 'version' keyword for convenience
    if argv == ["version"]:
        print(get_version_info())
        return 0

    # Support legacy 'pingx check <target>' transparently
    if argv and argv[0] == "check":
        argv = argv[1:]

    args = parser.parse_args(argv)

    if args.no_color:
        set_color_enabled(False)

    if args.show_version:
        print(get_version_info())
        return 0

    if not args.target:
        parser.print_help()
        return 0

    # Determine packet count (0 or negative means continuous ping until Ctrl+C)
    count = None if args.count is not None and args.count <= 0 else args.count

    try:
        pinger = ICMPPing(
            target=args.target,
            count=count,
            interval=args.interval,
            timeout=args.timeout,
            ipv4_only=args.ipv4,
            ipv6_only=args.ipv6,
        )
    except ValueError as e:
        print(f"{red('pingx: error:')} {e}", file=sys.stderr)
        return 1

    # Standard clean Linux ping output header
    print(f"PING {pinger.cleaned_target} ({pinger.resolved_ip}): {pinger.packet_size} data bytes\n")

    stream = pinger.ping_stream()
    interrupted = False

    def handle_sigint(signum, frame):
        nonlocal interrupted
        interrupted = True
        print("")  # Newline after Ctrl+C
        if stream.statistics:
            print("\n" + stream.statistics.summary_text())
        sys.exit(0)

    # Register graceful signal handler
    signal.signal(signal.SIGINT, handle_sigint)

    try:
        for packet in stream:
            print(packet.formatted_line())
    except KeyboardInterrupt:
        if not interrupted:
            print("")
            if stream.statistics:
                print("\n" + stream.statistics.summary_text())
        return 0

    # Print final summary statistics
    stats = stream.statistics
    if stats:
        print("\n" + stats.summary_text())
        return 0 if stats.received > 0 else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
