"""
Tests for ICMP packet building, checksums, and ping stream execution.
"""

import unittest
from pingx.icmp import ICMPPing, calculate_checksum


class TestICMPPing(unittest.TestCase):
    def test_checksum_calculation(self):
        data = b"\x08\x00\x00\x00\x12\x34\x00\x01testdata"
        ck = calculate_checksum(data)
        self.assertIsInstance(ck, int)
        self.assertGreaterEqual(ck, 0)
        self.assertLessEqual(ck, 0xFFFF)

    def test_invalid_parameters(self):
        # Flooding protection
        with self.assertRaises(ValueError):
            ICMPPing("127.0.0.1", interval=0.05)

        # Mutually exclusive v4 and v6
        with self.assertRaises(ValueError):
            ICMPPing("127.0.0.1", ipv4_only=True, ipv6_only=True)

    def test_localhost_ipv4_ping(self):
        pinger = ICMPPing("127.0.0.1", count=2, interval=0.2, timeout=1.0)
        stream = pinger.ping_stream()
        packets = list(stream)

        self.assertEqual(len(packets), 2)
        for pkt in packets:
            self.assertTrue(pkt.success)
            self.assertIsNotNone(pkt.rtt_ms)
            self.assertGreater(pkt.rtt_ms, 0.0)

        stats = stream.statistics
        self.assertEqual(stats.transmitted, 2)
        self.assertEqual(stats.received, 2)
        self.assertEqual(stats.packet_loss_pct, 0.0)

    def test_hostname_resolution(self):
        pinger = ICMPPing("localhost", count=1, interval=0.2, timeout=1.0)
        self.assertIn(pinger.resolved_ip, ["127.0.0.1", "::1"])


if __name__ == "__main__":
    unittest.main()
