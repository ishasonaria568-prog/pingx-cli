# PINGX — Lightweight Network Ping Utility

<p align="center">
  <strong>Simple. Lightweight. Powerful CLI Ping Tool.</strong>
</p>

<p align="center">
  Python | ICMP | IPv4 & IPv6 | Kali Linux
</p>

PINGX is a lightweight Python-based command-line utility for testing network connectivity using ICMP Echo Requests and Replies.

It provides essential network diagnostics, including response time, packet loss, TTL information and latency statistics directly from your terminal.

Developed by **Isha Sonaria**.

## Features

- ICMP Echo Request and Reply
- IPv4 and IPv6 support
- Hostname and IP address support
- Configurable packet count
- Configurable packet interval
- Response timeout control
- Round-trip time (RTT) measurement
- TTL information when available
- Packet transmission and reception statistics
- Packet loss percentage
- Minimum, average and maximum RTT
- Continuous ping with Ctrl+C interruption
- Lightweight terminal-based interface

## Installation — Kali Linux

### 1. Install prerequisites

```bash
sudo apt update
sudo apt install -y git python3 python3-pip pipx
```

### 2. Clone the repository

```bash
git clone https://github.com/ishasonaria568-prog/pingx-cli.git
```

### 3. Enter the repository

```bash
cd pingx-cli
```

### 4. Enter the actual Python project directory

**Important:** The Python application and `pyproject.toml` are located inside the `ping-tool/` directory.

```bash
cd ping-tool
```

### 5. Install PINGX using pipx

```bash
pipx install .
```

### 6. Verify installation

```bash
pingx --version
```

If the command is not found, run:

```bash
pipx ensurepath
```

Restart your terminal and try again.

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

### Configure response timeout

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

Press `Ctrl+C` to stop the operation and display the final statistics.

### Display help

```bash
pingx --help
```

### Display version

```bash
pingx --version
```

*Note: Available options depend on the implemented CLI arguments. Refer to `pingx --help` for the exact supported syntax.*

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

*Example output is illustrative.*

## Project Structure

```text
pingx-cli/
├── README.md
├── metadata.json
└── ping-tool/
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
    └── LICENSE
```

## Run Tests

Navigate to the Python project directory:

```bash
cd ~/pingx-cli/ping-tool
```

Run the test suite:

```bash
python3 -m unittest discover tests -v
```

## Uninstallation

To uninstall PINGX:

```bash
pipx uninstall pingx
```

## Technical Details

| Component | Technology |
|---|---|
| Programming Language | Python |
| Network Protocol | ICMP / ICMPv6 |
| CLI | argparse |
| Networking | Python socket |
| Packaging | setuptools |
| Installation | pipx |
| Primary Platform | Kali Linux |

## Responsible Usage

PINGX is intended for legitimate network connectivity testing and troubleshooting.

Use it only on networks and systems you own or have permission to test. Avoid excessive packet transmission.

## Developer

**Isha Sonaria**

- GitHub: https://github.com/ishasonaria568-prog
- Repository: https://github.com/ishasonaria568-prog/pingx-cli
- Tool: PINGX
- Version: 1.0.0
- License: MIT

---

<p align="center">
  <strong>PINGX — Network Diagnostics, Straight from Your Terminal.</strong>
</p>
