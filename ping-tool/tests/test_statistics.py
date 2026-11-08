"""
Tests for PingStatistics calculations and summary output.
"""

import unittest
from pingx.statistics import PingStatistics


class TestPingStatistics(unittest.TestCase):
    def test_empty_statistics(self):
        stats = PingStatistics(target="example.com", target_ip="93.184.216.34")
        self.assertEqual(stats.transmitted, 0)
        self.assertEqual(stats.received, 0)
        self.assertEqual(stats.lost, 0)
        self.assertEqual(stats.packet_loss_pct, 0.0)
        self.assertIsNone(stats.min_rtt)
        self.assertIsNone(stats.avg_rtt)
        self.assertIsNone(stats.max_rtt)

    def test_perfect_success(self):
        stats = PingStatistics(target="127.0.0.1", target_ip="127.0.0.1")
        stats.add_success(10.0, ttl=64)
        stats.add_success(20.0, ttl=64)
        stats.add_success(30.0, ttl=64)

        self.assertEqual(stats.transmitted, 3)
        self.assertEqual(stats.received, 3)
        self.assertEqual(stats.lost, 0)
        self.assertEqual(stats.packet_loss_pct, 0.0)
        self.assertEqual(stats.min_rtt, 10.0)
        self.assertEqual(stats.avg_rtt, 20.0)
        self.assertEqual(stats.max_rtt, 30.0)
        self.assertAlmostEqual(stats.mdev_rtt, 8.1649, places=3)

    def test_packet_loss_calculation(self):
        stats = PingStatistics(target="test.local", target_ip="192.168.1.50")
        stats.add_success(15.0)
        stats.add_loss()
        stats.add_loss()
        stats.add_success(25.0)

        self.assertEqual(stats.transmitted, 4)
        self.assertEqual(stats.received, 2)
        self.assertEqual(stats.lost, 2)
        self.assertEqual(stats.packet_loss_pct, 50.0)

    def test_summary_text_output(self):
        stats = PingStatistics(target="google.com", target_ip="142.250.190.46")
        stats.add_success(23.81, ttl=117)
        stats.add_success(24.32, ttl=117)
        stats.add_success(25.10, ttl=117)
        stats.add_success(24.05, ttl=117)

        summary = stats.summary_text()
        self.assertIn("--- google.com ping statistics ---", summary)
        self.assertIn("4 packets transmitted, 4 received, 0% packet loss", summary)
        self.assertIn("rtt min/avg/max/mdev =", summary)


if __name__ == "__main__":
    unittest.main()
