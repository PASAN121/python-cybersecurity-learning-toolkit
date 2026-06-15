# 🔍 PyPortScanner — Multithreaded TCP Port Scanner with Banner Grabbing

A lightweight, efficient command-line **TCP Connect Port Scanner** built in Python. It combines concurrent scanning, service banner detection, and structured JSON reporting to provide quick reconnaissance of open ports and running services on a target host.

This tool is designed for **network administrators, penetration testers, and cybersecurity learners** who need a fast, dependency-free utility for basic host enumeration.

> ⚠️ **Disclaimer:** This tool is intended for educational purposes and authorized security testing only. Scanning systems without explicit permission is illegal. Use responsibly.

---

## ✨ Features

- ✅ **CLI-based input** — specify target IP and port range directly from the terminal
- ✅ **Input validation** — verifies IPv4 address format and ensures a valid port range
- ✅ **TCP Connect Scan** — uses `socket.connect_ex()` for reliable full-handshake detection
- ✅ **Concurrent scanning with ThreadPoolExecutor** — efficiently manages a pool of up to 100 worker threads for fast, scalable scanning
- ✅ **Live progress tracking** — displays real-time scan progress (`completed/total`) in the terminal
- ✅ **Banner grabbing** — attempts to read service banners from open ports for fingerprinting
- ✅ **Structured results** — collects scan data as a list of dictionaries (`port`, `status`, `banner`)
- ✅ **JSON reporting** — generates machine-readable output for integration with other tools
- ✅ **Scan history tracking** — saves timestamped scan logs for auditing and comparison

---

## 🏗️ How It Works

1. **Input Validation**
   The provided IP address is checked for valid IPv4 formatting (four octets, each 0–255), and the port range is validated to ensure the start port does not exceed the end port.

2. **Concurrent Port Scanning**
   For each port in the specified range, a task is submitted to a `ThreadPoolExecutor` (up to 100 concurrent workers). Each task attempts a TCP connection using `socket.connect_ex()`. A return value of `0` indicates the port is **open**. As each task completes, a live progress counter (`completed/total`) is printed to the terminal.

3. **Banner Grabbing**
   For every open port, the scanner attempts a secondary connection and reads up to 1024 bytes from the socket, capturing any service banner (e.g., SSH version strings, HTTP headers) within a 2-second timeout.

4. **Result Aggregation**
   Results from completed tasks are filtered (only open ports return data) and collected into a list, which is sorted numerically once all tasks complete.

5. **Reporting**
   - The latest scan results overwrite `reports/latest_scan.json`
   - A timestamped copy is stored in `reports/history/scan_YYYY-MM-DD_HH-MM-SS.json` for historical record-keeping

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- No external dependencies — uses only the Python standard library

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/pyportscanner.git
cd pyportscanner

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

No `pip install` is required — the project relies entirely on Python's built-in modules (`socket`, `threading`, `argparse`, `json`, `os`, `datetime`).

---

## 🚀 Usage

### Basic Syntax

```bash
python scanner.py <target_ip> <start_port> <end_port>
```

### Examples

**Scan common ports on localhost:**
```bash
python scanner.py 127.0.0.1 1 1024
```

**Scan a specific port range on a target host:**
```bash
python scanner.py 192.168.1.10 20 100
```

**Scan a single port:**
```bash
python scanner.py 192.168.1.10 80 80
```

### Sample Terminal Output

```
Target IP: 192.168.1.10
Port Range: 20 - 100
----------------------------------------

Scanning 81 ports...

Progress: 81/81
Scan completed.

Open Ports + Services:

Port 22 is Open
    Banner: SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6

Port 80 is Open
    Banner: No banner received
```

---

## 📄 Example Output (JSON)

Each scan generates a JSON report saved under `reports/latest_scan.json`:

```json
[
  {
    "port": 22,
    "status": "Open",
    "banner": "SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.6"
  },
  {
    "port": 80,
    "status": "Open",
    "banner": "No banner received"
  },
  {
    "port": 443,
    "status": "Open",
    "banner": "No banner / filtered / timeout"
  }
]
```

A timestamped copy of this report is also stored in `reports/history/` for auditing past scans, e.g.:

```
reports/history/scan_2026-06-16_14-32-05.json
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3** | Core programming language |
| `concurrent.futures` (ThreadPoolExecutor) | Managed thread pool for concurrent, scalable scanning |
| `socket` | Low-level TCP connection handling and banner grabbing |
| `argparse` | Command-line argument parsing |
| `json` | Structured report generation |
| `datetime` / `os` | Timestamped history file management |

---

## 📚 Learning Outcomes

This project demonstrates practical knowledge of both **networking/cybersecurity fundamentals** and **Python software engineering practices**:

### 🔐 Cybersecurity Concepts
- TCP three-way handshake and connection-based port scanning
- Differences between open, closed, and filtered ports
- Service/banner enumeration for fingerprinting and reconnaissance
- Building blocks of basic network reconnaissance tools used in penetration testing

### 🐍 Python Concepts
- Socket programming (`AF_INET`, `SOCK_STREAM`, `connect_ex`, timeouts)
- Concurrent programming with `ThreadPoolExecutor` and `as_completed` for I/O-bound tasks
- Robust input validation and error handling
- CLI tool design with `argparse`
- Structured data handling and JSON serialization
- File system operations for persistent logging and reporting

---

## 🗺️ Roadmap / Future Improvements

- [ ] Add UDP scanning support
- [ ] Implement service fingerprinting database for known port/banner combinations
- [ ] Add export formats (CSV, HTML report)
- [ ] Add scan rate limiting / stealth scan options
- [ ] Multi-host scanning support

---

## 📃 License

This project is licensed under the MIT License — feel free to use, modify, and distribute with attribution.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a pull request or submit an issue.