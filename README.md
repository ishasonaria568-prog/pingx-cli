# PINGX — Lightweight Network Ping Utility

<p align="center">
  <strong>A Simple. Lightweight. Powerful CLI Ping Tool.</strong>
</p>

<p align="center">
  Built with Python | Designed for Kali Linux | MIT License
</p>

**PINGX** is a lightweight, standalone Python-based command-line utility for testing network connectivity using ICMP Echo Requests and Replies. It provides essential network reachability information, response times, packet loss, and latency statistics directly in your terminal.

Developed by **Isha Sonaria**.

## Features

- **ICMP Ping:** Send ICMP Echo Requests and receive Echo Replies.
- **IPv4 & IPv6:** Supports both IPv4 and IPv6 networking.
- **DNS Resolution:** Resolve hostnames before sending packets.
- **Packet Control:** Configure packet count and sending interval.
- **Timeout Control:** Set the maximum waiting time for responses.
- **RTT Measurement:** Display packet round-trip time in milliseconds.
- **TTL Information:** Display TTL values when available.
- **Packet Statistics:** View transmitted packets, received packets, and packet loss.
- **Latency Statistics:** Calculate minimum, average, maximum, and mean deviation (mdev).
- **Continuous Ping:** Continue sending packets until interrupted using `Ctrl+C`.
- **Lightweight:** Uses Python standard libraries without external Python dependencies.
- **Terminal Friendly:** Clean output with optional ANSI colors.

## Installation — Kali Linux

### 1. Install requirements

```bash
sudo apt update
sudo apt install -y git python3 python3-pip pipx
```

### 2. Clone the repository

```bash
git clone https://github.com/ishasonaria568-prog/pingx-cli.git
```

### 3. Enter the project directory

```bash
cd pingx-cli
```

### 4. Install using pipx

```bash
pipx install .
```

### 5. Verify installation

```bash
pingx --version
```

If the command is not found, ensure pipx's binary directory is added to your PATH:

```bash
pipx ensurepath
```

Restart your terminal if required.

## Usage

### Basic ping

```bash
pingx google.com
```

### Ping localhost

```bash
pingx 127.0.0.1
```

### Send a specific number of packets

```bash
pingx google.com -c 5
```

### Set packet interval

```bash
pingx google.com -c 10 -i 1
```

### Set response timeout

```bash
pingx google.com -W 3
```

### Force IPv4

```bash
pingx google.com -4
```

### Force IPv6

```bash
pingx google.com -6
```

### Disable terminal colors

```bash
pingx google.com --no-color
```

### Continuous ping

```bash
pingx google.com -c 0
```

Press `Ctrl+C` to stop continuous ping and display the final statistics.

### View help

```bash
pingx --help
```

### View version

```bash
pingx --version
```

## Example Output

```text
PING google.com (142.250.x.x): 56 data bytes

64 bytes from 142.250.x.x: icmp_seq=1 ttl=117 time=24.32 ms
64 bytes from 142.250.x.x: icmp_seq=2 ttl=117 time=23.81 ms
64 bytes from 142.250.x.x: icmp_seq=3 ttl=117 time=25.10 ms
64 bytes from 142.250.x.x: icmp_seq=4 ttl=117 time=24.05 ms

--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss
rtt min/avg/max/mdev = 23.810/24.320/25.100/0.481 ms
```

*Output values above are illustrative.*

## Project Structure

```text
pingx-cli/
├── pingx/
│   ├── __init__.py
│   ├── cli.py
│   ├── icmp.py
│   ├── statistics.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_icmp.py
│   └── test_statistics.py
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

## Run Tests

Run the test suite using Python's built-in unittest framework:

```bash
python3 -m unittest discover tests -v
```

## Technical Details

| Component | Technology |
|---|---|
| Language | Python |
| Protocol | ICMP / ICMPv6 |
| CLI Framework | argparse |
| Networking | socket, select |
| Statistics | Python |
| Packaging | setuptools |
| Installation | pipx |
| Primary Platform | Kali Linux |

## Responsible Usage

PINGX is designed for legitimate network connectivity testing and troubleshooting.

Use it only on systems and networks you own or have permission to test. Respect network policies and avoid excessive packet transmission.

## Developer

**Isha Sonaria**

- GitHub: https://github.com/ishasonaria568-prog
- Tool: PINGX
- Version: 1.0.0
- License: MIT

---

<p align="center">
  <strong>PINGX — Simple Network Diagnostics, Straight from Your Terminal.</strong>
</p>
