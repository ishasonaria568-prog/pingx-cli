# PING — Lightweight Standalone Network Diagnostics CLI Tool

```text
PING v1.0.0 (pingx) — Lightweight Network Diagnostic Utility
Built by Isha Sonaria (https://github.com/ishasonaria568-prog)
Platform priority: Kali Linux | MIT License
```

**PING** (executable: `pingx`) is a minimal, lightweight, standalone Python network diagnostic CLI utility designed for **Kali Linux** and other UNIX/Linux operating systems, similar to the traditional Linux `ping` command.

Developed by **Isha Sonaria** ([GitHub Profile](https://github.com/ishasonaria568-prog)).

---

## ⚡ Features

- **ICMP Echo Probing**: Standard RFC 792 (IPv4 ICMP) and RFC 4443 (ICMPv6) echo request and reply.
- **Dual Stack**: Seamless IPv4 and IPv6 support with `-4` and `-6` enforcement flags.
- **Microsecond Precision**: Accurate Round-Trip Time (RTT) measurements with min, max, average, and jitter (`mdev`) metrics.
- **TTL Display**: Time-To-Live (TTL) hop observation.
- **Configurable Probing**: Configurable packet count (`-c`), interval (`-i`), and timeout (`-W`).
- **Continuous Mode**: Continuous probing with safe, graceful interruption using `Ctrl+C`.
- **Zero External Dependencies**: Built entirely using Python standard libraries (`socket`, `struct`, `select`, `subprocess`, `argparse`).
- **Terminal Friendly**: Clean, readable terminal output with subtle color cues and `--no-color` support.

---

## 🚀 Installation on Kali Linux

### Method 1: Using pipx (Recommended for Kali Linux)

Kali Linux (Debian 12+) enforces PEP 668 externally managed environments. Using `pipx` ensures clean, isolated installation:

```bash
# 1. Install pipx if not already present
sudo apt update && sudo apt install -y pipx git

# 2. Clone the repository
git clone https://github.com/ishasonaria568-prog/ping-tool.git
cd ping-tool

# 3. Install pingx globally in user path
pipx install .

# 4. Ensure pipx binary directory is in your PATH
pipx ensurepath

# 5. Verify installation
pingx --version
```

### Method 2: Standard pip or Developer Editable Mode

```bash
cd ping-tool
pip install -e .

# Or install directly:
pip install .
```

---

## 💻 CLI Usage

```bash
# Basic reachability check (default: 4 packets)
pingx google.com
pingx 127.0.0.1

# Custom packet count
pingx google.com -c 5

# Custom packet count and interval (seconds)
pingx google.com -c 10 -i 1

# Custom timeout (seconds)
pingx google.com -W 3

# Force IPv4 only
pingx google.com -4

# Force IPv6 only
pingx google.com -6

# Disable terminal colors
pingx google.com --no-color

# View help and version
pingx --help
pingx --version
```

### Example Terminal Output

```text
$ pingx google.com
PING google.com (142.250.190.46): 56 data bytes

64 bytes from 142.250.190.46: icmp_seq=1 ttl=117 time=24.32 ms
64 bytes from 142.250.190.46: icmp_seq=2 ttl=117 time=23.81 ms
64 bytes from 142.250.190.46: icmp_seq=3 ttl=117 time=25.10 ms
64 bytes from 142.250.190.46: icmp_seq=4 ttl=117 time=24.05 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
rtt min/avg/max/mdev = 23.810/24.320/25.100/0.481 ms
```

---

## 🧪 Running Unit Tests

Run the complete test suite using Python's standard `unittest`:

```bash
cd ping-tool
python3 -m unittest discover tests -v
```

---

## 📁 Repository Structure

```text
ping-tool/
├── pingx/
│   ├── __init__.py         # Package exports & version
│   ├── cli.py              # Lightweight Linux-style CLI interface
│   ├── icmp.py             # ICMP Echo Request & Reply engine
│   ├── statistics.py       # Latency, packet loss & jitter metrics
│   └── utils.py            # ANSI colors & input validators
├── tests/
│   ├── test_cli.py         # CLI argument & execution tests
│   ├── test_icmp.py        # ICMP packet & socket tests
│   └── test_statistics.py  # Statistics & math tests
├── pyproject.toml          # Build configuration & entry point (pingx)
├── README.md               # Documentation & usage manual
├── LICENSE                 # MIT License
└── .gitignore
```

---

## 👤 Author & License

- **Developer**: Isha Sonaria
- **GitHub**: [https://github.com/ishasonaria568-prog](https://github.com/ishasonaria568-prog)
- **License**: MIT License
