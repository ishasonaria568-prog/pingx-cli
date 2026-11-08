"""
PING — Lightweight Standalone Network Diagnostics CLI Tool
ICMP Echo Request/Reply protocol implementation (IPv4 & IPv6).
Author: Isha Sonaria (https://github.com/ishasonaria568-prog)
"""

import os
import sys
import time
import struct
import select
import socket
import subprocess
from dataclasses import dataclass
from typing import Optional, Generator, Tuple
from .utils import (
    validate_target,
    format_ms,
    red,
)
from .statistics import PingStatistics

# ICMP Protocol Constants
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP6_ECHO_REQUEST = 128
ICMP6_ECHO_REPLY = 129


@dataclass
class PingPacketResult:
    """Result of a single ICMP echo probe."""

    seq: int
    success: bool
    target: str
    ip: str
    rtt_ms: Optional[float] = None
    ttl: Optional[int] = None
    bytes_count: int = 64
    error_message: Optional[str] = None

    def formatted_line(self) -> str:
        """Format standard Linux ping style per-packet response line."""
        if self.success and self.rtt_ms is not None:
            ttl_str = f"ttl={self.ttl} " if self.ttl is not None else ""
            return (
                f"{self.bytes_count} bytes from {self.ip}: "
                f"icmp_seq={self.seq} {ttl_str}time={format_ms(self.rtt_ms)}"
            )
        else:
            msg = self.error_message or "Request timeout"
            return f"{msg} for icmp_seq {self.seq}"


def calculate_checksum(data: bytes) -> int:
    """Calculate RFC 1071 standard internet checksum."""
    count_to = (len(data) // 2) * 2
    count = 0
    total = 0

    while count < count_to:
        total += (data[count + 1] << 8) + data[count]
        count += 2

    if count_to < len(data):
        total += data[len(data) - 1]

    total = (total >> 16) + (total & 0xFFFF)
    total += total >> 16
    answer = ~total & 0xFFFF
    return (answer >> 8) | ((answer & 0xFF) << 8)


class PingStream:
    """
    Iterator over PingPacketResult instances that exposes .statistics.
    Supports both streaming iteration and direct access to cumulative statistics.
    """

    def __init__(self, pinger: "ICMPPing"):
        self.pinger = pinger
        self.statistics = PingStatistics(target=pinger.cleaned_target, target_ip=pinger.resolved_ip)
        self.value = self.statistics
        self._generator = self._execute()

    def __iter__(self):
        return self

    def __next__(self) -> PingPacketResult:
        return next(self._generator)

    def _execute(self) -> Generator[PingPacketResult, None, None]:
        stats = self.statistics
        pinger = self.pinger
        stats.start_time = time.time()

        sock = None
        use_socket = True
        try:
            if pinger.is_ipv6:
                proto = socket.IPPROTO_ICMPV6
                family = socket.AF_INET6
            else:
                proto = socket.IPPROTO_ICMP
                family = socket.AF_INET

            try:
                sock = socket.socket(family, socket.SOCK_RAW, proto)
            except PermissionError:
                sock = socket.socket(family, socket.SOCK_DGRAM, proto)
            sock.setblocking(False)
        except Exception:
            use_socket = False
            sock = None

        pid = os.getpid() & 0xFFFF
        seq = 1

        try:
            while True:
                if pinger.count is not None and pinger.count > 0 and seq > pinger.count:
                    break

                if use_socket and sock:
                    packet_res = pinger._send_socket_ping_packet(sock, seq, pid)
                else:
                    packet_res = pinger._send_system_ping_packet(seq)

                if packet_res.success and packet_res.rtt_ms is not None:
                    stats.add_success(packet_res.rtt_ms, packet_res.ttl)
                else:
                    stats.add_loss()

                yield packet_res

                seq += 1
                if pinger.count is None or pinger.count <= 0 or seq <= pinger.count:
                    time.sleep(pinger.interval)

        finally:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass
            stats.end_time = time.time()


class ICMPPing:
    """
    Lightweight, reliable ICMP Ping engine with dual-mode execution:
    1. Direct native Python ICMP socket.
    2. Subprocess ping fallback for unprivileged Linux environments.
    """

    def __init__(
        self,
        target: str,
        count: Optional[int] = 4,
        interval: float = 1.0,
        timeout: float = 2.0,
        ipv4_only: bool = False,
        ipv6_only: bool = False,
        packet_size: int = 56,
    ):
        if ipv4_only and ipv6_only:
            raise ValueError("Cannot specify both -4 (IPv4) and -6 (IPv6) modes simultaneously.")

        if interval < 0.2:
            raise ValueError("Interval cannot be less than 0.2s to prevent network flooding.")
        if timeout < 0.1:
            raise ValueError("Timeout cannot be less than 0.1s.")

        self.raw_target = target
        self.count = count  # None or 0 means continuous ping
        self.interval = interval
        self.timeout = timeout
        self.ipv4_only = ipv4_only
        self.ipv6_only = ipv6_only
        self.packet_size = min(max(packet_size, 16), 1472)
        self.statistics: Optional[PingStatistics] = None

        self.cleaned_target, self.target_type = validate_target(target)
        self.resolved_ip, self.is_ipv6 = self._resolve_target()

    def _resolve_target(self) -> Tuple[str, bool]:
        """Resolve target to IP address respecting -4 and -6 flags."""
        if self.target_type == "ipv4":
            if self.ipv6_only:
                raise ValueError(f"Target '{self.cleaned_target}' is IPv4, but -6 was requested.")
            return self.cleaned_target, False

        if self.target_type == "ipv6":
            if self.ipv4_only:
                raise ValueError(f"Target '{self.cleaned_target}' is IPv6, but -4 was requested.")
            return self.cleaned_target, True

        family = socket.AF_UNSPEC
        if self.ipv4_only:
            family = socket.AF_INET
        elif self.ipv6_only:
            family = socket.AF_INET6

        try:
            addr_info = socket.getaddrinfo(self.cleaned_target, None, family, socket.SOCK_STREAM)
        except socket.gaierror as e:
            raise ValueError(f"Cannot resolve '{self.cleaned_target}': {e.strerror}")

        if not addr_info:
            raise ValueError(f"No address found for target '{self.cleaned_target}'.")

        selected = addr_info[0]
        ip = selected[4][0]
        is_v6 = selected[0] == socket.AF_INET6
        return ip, is_v6

    def _send_system_ping_packet(self, seq: int) -> PingPacketResult:
        """Subprocess ping execution fallback without shell interpolation."""
        cmd = ["ping6" if self.is_ipv6 and subprocess.run(["which", "ping6"], capture_output=True).returncode == 0 else "ping"]
        if self.is_ipv6:
            cmd.append("-6")
        else:
            cmd.append("-4")

        cmd.extend(["-c", "1", "-W", str(max(1, int(self.timeout))), self.resolved_ip])

        t_start = time.perf_counter()
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout + 1.0,
            )
            rtt = (time.perf_counter() - t_start) * 1000.0

            if res.returncode == 0:
                ttl = None
                time_val = rtt
                for token in res.stdout.split():
                    if token.lower().startswith("ttl="):
                        try:
                            ttl = int(token.split("=")[1])
                        except ValueError:
                            pass
                    elif token.lower().startswith("time="):
                        try:
                            time_val = float(token.split("=")[1].replace("ms", ""))
                        except ValueError:
                            pass
                return PingPacketResult(
                    seq=seq,
                    success=True,
                    target=self.cleaned_target,
                    ip=self.resolved_ip,
                    rtt_ms=time_val,
                    ttl=ttl or 64,
                    bytes_count=64,
                )
            else:
                return PingPacketResult(
                    seq=seq,
                    success=False,
                    target=self.cleaned_target,
                    ip=self.resolved_ip,
                    error_message="Request timeout",
                )
        except subprocess.TimeoutExpired:
            return PingPacketResult(
                seq=seq,
                success=False,
                target=self.cleaned_target,
                ip=self.resolved_ip,
                error_message="Request timeout",
            )
        except Exception as e:
            return PingPacketResult(
                seq=seq,
                success=False,
                target=self.cleaned_target,
                ip=self.resolved_ip,
                error_message=str(e),
            )

    def _send_socket_ping_packet(self, sock: socket.socket, seq: int, pid: int) -> PingPacketResult:
        """Direct ICMP socket probe."""
        if self.is_ipv6:
            icmp_type = ICMP6_ECHO_REQUEST
        else:
            icmp_type = ICMP_ECHO_REQUEST

        icmp_code = 0
        checksum = 0
        payload = struct.pack("!d", time.time()) + (b"Q" * (self.packet_size - 8))
        header = struct.pack("!BBHHH", icmp_type, icmp_code, checksum, pid, seq)

        if not self.is_ipv6:
            checksum = calculate_checksum(header + payload)
            header = struct.pack("!BBHHH", icmp_type, icmp_code, checksum, pid, seq)

        packet = header + payload
        dest_addr = (self.resolved_ip, 1)

        t_send = time.perf_counter()
        try:
            sock.sendto(packet, dest_addr)
        except socket.error as e:
            return PingPacketResult(
                seq=seq,
                success=False,
                target=self.cleaned_target,
                ip=self.resolved_ip,
                error_message=f"Send failed: {e}",
            )

        while True:
            remaining = self.timeout - (time.perf_counter() - t_send)
            if remaining <= 0:
                return PingPacketResult(
                    seq=seq,
                    success=False,
                    target=self.cleaned_target,
                    ip=self.resolved_ip,
                    error_message="Request timeout",
                )

            readable, _, _ = select.select([sock], [], [], remaining)
            if not readable:
                return PingPacketResult(
                    seq=seq,
                    success=False,
                    target=self.cleaned_target,
                    ip=self.resolved_ip,
                    error_message="Request timeout",
                )

            recv_time = time.perf_counter()
            try:
                data, _ = sock.recvfrom(1500)
            except socket.error:
                return PingPacketResult(
                    seq=seq,
                    success=False,
                    target=self.cleaned_target,
                    ip=self.resolved_ip,
                    error_message="Request timeout",
                )

            ttl = None
            if not self.is_ipv6:
                ip_header_len = (data[0] & 0x0F) * 4
                ttl = data[8]
                icmp_packet = data[ip_header_len:]
            else:
                icmp_packet = data

            if len(icmp_packet) < 8:
                continue

            r_type, _, _, r_id, _ = struct.unpack("!BBHHH", icmp_packet[:8])

            expected_type = ICMP6_ECHO_REPLY if self.is_ipv6 else ICMP_ECHO_REPLY
            if r_type == expected_type and (r_id == pid or r_id == 0):
                rtt = (recv_time - t_send) * 1000.0
                return PingPacketResult(
                    seq=seq,
                    success=True,
                    target=self.cleaned_target,
                    ip=self.resolved_ip,
                    rtt_ms=rtt,
                    ttl=ttl or 64,
                    bytes_count=len(icmp_packet),
                )
            elif r_type == 3:  # Unreachable
                return PingPacketResult(
                    seq=seq,
                    success=False,
                    target=self.cleaned_target,
                    ip=self.resolved_ip,
                    error_message="Destination Host Unreachable",
                )

    def ping_stream(self) -> PingStream:
        """Returns stream iterator over packet responses with .statistics."""
        stream = PingStream(self)
        self.statistics = stream.statistics
        return stream
