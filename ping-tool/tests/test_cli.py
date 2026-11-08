"""
Tests for CLI argument parsing and execution.
"""

import io
import sys
import unittest
from pingx.cli import main, build_parser


class TestCLI(unittest.TestCase):
    def test_parser_standard_ping(self):
        parser = build_parser()
        args = parser.parse_args(["google.com", "-c", "5", "-i", "1.0", "-W", "3.0"])
        self.assertEqual(args.target, "google.com")
        self.assertEqual(args.count, 5)
        self.assertEqual(args.interval, 1.0)
        self.assertEqual(args.timeout, 3.0)

    def test_version_flag(self):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            code = main(["--version"])
            output = sys.stdout.getvalue()
            self.assertEqual(code, 0)
            self.assertIn("PING v1.0.0", output)
            self.assertIn("Isha Sonaria", output)
        finally:
            sys.stdout = old_stdout

    def test_ping_localhost(self):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            code = main(["127.0.0.1", "-c", "2", "-i", "0.2"])
            output = sys.stdout.getvalue()
            self.assertEqual(code, 0)
            self.assertIn("PING 127.0.0.1 (127.0.0.1): 56 data bytes", output)
            self.assertIn("bytes from 127.0.0.1", output)
            self.assertIn("--- 127.0.0.1 ping statistics ---", output)
        finally:
            sys.stdout = old_stdout

    def test_ping_ipv4_flag(self):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            code = main(["127.0.0.1", "-4", "-c", "1", "-i", "0.2"])
            output = sys.stdout.getvalue()
            self.assertEqual(code, 0)
            self.assertIn("64 bytes from 127.0.0.1", output)
        finally:
            sys.stdout = old_stdout


if __name__ == "__main__":
    unittest.main()
