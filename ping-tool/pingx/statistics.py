"""
PING — Lightweight Standalone Network Diagnostics CLI Tool
Statistics calculation and metrics tracking for ICMP packet transmissions.
Author: Isha Sonaria (https://github.com/ishasonaria568-prog)
"""

import math
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PingStatistics:
    """Calculates and formats standard ping statistics."""

    target: str
    target_ip: str
    transmitted: int = 0
    received: int = 0
    rtts: List[float] = field(default_factory=list)
    ttl_values: List[int] = field(default_factory=list)
    start_time: float = 0.0
    end_time: float = 0.0

    def add_success(self, rtt_ms: float, ttl: Optional[int] = None) -> None:
        """Record a successful packet reply."""
        self.transmitted += 1
        self.received += 1
        self.rtts.append(rtt_ms)
        if ttl is not None and ttl > 0:
            self.ttl_values.append(ttl)

    def add_loss(self) -> None:
        """Record a lost or dropped packet."""
        self.transmitted += 1

    @property
    def lost(self) -> int:
        return max(0, self.transmitted - self.received)

    @property
    def packet_loss_pct(self) -> float:
        if self.transmitted == 0:
            return 0.0
        return (self.lost / self.transmitted) * 100.0

    @property
    def min_rtt(self) -> Optional[float]:
        return min(self.rtts) if self.rtts else None

    @property
    def max_rtt(self) -> Optional[float]:
        return max(self.rtts) if self.rtts else None

    @property
    def avg_rtt(self) -> Optional[float]:
        return (sum(self.rtts) / len(self.rtts)) if self.rtts else None

    @property
    def mdev_rtt(self) -> Optional[float]:
        """Calculate mean deviation (jitter / standard deviation)."""
        if not self.rtts or len(self.rtts) < 2:
            return 0.0 if self.rtts else None
        avg = self.avg_rtt or 0.0
        variance = sum((x - avg) ** 2 for x in self.rtts) / len(self.rtts)
        return math.sqrt(variance)

    def summary_text(self) -> str:
        """
        Generate standard Linux ping style summary:
        --- google.com ping statistics ---
        4 packets transmitted, 4 received, 0% packet loss
        rtt min/avg/max/mdev = 23.810/24.320/25.100/0.481 ms
        """
        lines = [f"--- {self.target} ping statistics ---"]

        loss_pct = self.packet_loss_pct
        loss_str = f"{int(loss_pct)}%" if loss_pct.is_integer() else f"{loss_pct:.1f}%"
        lines.append(
            f"{self.transmitted} packets transmitted, {self.received} received, {loss_str} packet loss"
        )

        if self.rtts and self.min_rtt is not None and self.avg_rtt is not None and self.max_rtt is not None and self.mdev_rtt is not None:
            lines.append(
                f"rtt min/avg/max/mdev = {self.min_rtt:.3f}/{self.avg_rtt:.3f}/{self.max_rtt:.3f}/{self.mdev_rtt:.3f} ms"
            )

        return "\n".join(lines)
