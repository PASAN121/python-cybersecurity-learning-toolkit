# 🕵️ Scapy Network Sniffer & Traffic Analyser

> **Python Cybersecurity Learning Toolkit** · Pasan Chandima (PASAN121)

A command-line packet capture and analysis tool built with [Scapy](https://scapy.net/). Supports both **live interface sniffing** and **offline PCAP file analysis**, with real-time port scan detection, JSONL traffic logging, and a session summary report.

---

## 📸 Demo Output

```
[INFO] Capturing on interface: eth0
[INFO] Filter: tcp
[INFO] Logging to: traffic_20250623_142301.json
[INFO] Press Ctrl+C to stop capture

[TCP]  192.168.1.10:54231  ->  93.184.216.34:443
[TCP]  192.168.1.10:54232  ->  93.184.216.34:80
[UDP]  192.168.1.1:53      ->  192.168.1.10:5353

[ALERT] Possible port scan from 10.0.0.5 (12 unique ports in 30s)

==================================================
  CAPTURE SUMMARY
==================================================
  Total packets logged : 143
    OTHER  : 5
    TCP    : 121
    UDP    : 17
  Unique source IPs    : 8
  Alerts raised        : 1

  [ALERT DETAILS]
    - 10.0.0.5 hit 12 unique ports

  Log saved to: traffic_20250623_142301.json
==================================================
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔴 Live capture | Sniff packets in real time from any network interface |
| 📂 PCAP analysis | Replay and analyse saved `.pcap` / `.pcapng` files |
| 🔍 Protocol filter | Isolate `tcp`, `udp`, or capture `all` traffic |
| 🚨 Port scan detection | Alerts when a source IP hits ≥ 10 unique ports within 30 s |
| 📝 JSONL logging | Every packet written as a JSON object to a timestamped log |
| 📊 Session summary | Packet counts, unique IPs, and alert breakdown at exit |

---

## 🐍 Python Learning Outcomes

This module covers a range of intermediate Python and software-design concepts.

### 1. `argparse` — CLI Argument Parsing

Build professional command-line interfaces with flags, choices, and help text.

```python
parser.add_argument("--mode", choices=["live", "pcap"])
parser.add_argument("--filter", default="all", choices=["tcp", "udp", "all"])
parser.add_argument("--list-ifaces", action="store_true")
```

**Concepts:** subcommands, default values, boolean flags (`store_true`), input validation.

---

### 2. Classes & OOP — `TrafficTracker`

A class used to maintain **stateful per-session tracking** of packet activity.

```python
class TrafficTracker:
    PORT_THRESHOLD = 10      # class-level constant
    TIME_WINDOW    = 30      # seconds

    def __init__(self):
        self.timestamps = defaultdict(list)
        self.dst_ports  = defaultdict(set)
        self.alerts     = []

    def update(self, packet_data): ...
    def _check_port_scan(self, src_ip, now): ...
```

**Concepts:** `__init__`, instance vs. class attributes, public/private method naming (`_check_port_scan`), encapsulation.

---

### 3. `collections.defaultdict`

A dictionary that auto-initialises missing keys, used to group timestamps and ports by source IP without `KeyError`.

```python
from collections import defaultdict

self.timestamps = defaultdict(list)   # {ip: [t1, t2, ...]}
self.dst_ports  = defaultdict(set)    # {ip: {port1, port2, ...}}
```

**Concept:** factory-based default values (`list`, `set`), avoiding boilerplate `if key not in dict` guards.

---

### 4. Closures & Higher-Order Functions

`make_packet_handler()` is a **factory function** — it returns an inner function (`packet_handler`) that "closes over" the `log_file` and `tracker` variables from the outer scope.

```python
def make_packet_handler(log_file, tracker):   # outer function
    def packet_handler(packet):               # inner function (closure)
        ...
        tracker.update(packet_data)           # captures outer variables
    return packet_handler
```

**Concepts:** closures, returning functions, callback design pattern (Scapy's `prn=` parameter).

---

### 5. File I/O — JSONL Logging

Each captured packet is appended to a log file as a single JSON line (newline-delimited JSON / JSONL format), making logs easy to stream and parse.

```python
import json

with open(log_file, "a") as f:
    f.write(json.dumps(packet_data) + "\n")

# Reading back:
with open(log_file, "r") as f:
    for line in f:
        entry = json.loads(line)
```

**Concepts:** `json.dumps` / `json.loads`, append mode (`"a"`), JSONL as a log format.

---

### 6. `datetime` & Timestamped Filenames

Each run generates a unique log filename so previous sessions are never overwritten.

```python
from datetime import datetime

def create_log_filename(base_name):
    name, ext = os.path.splitext(base_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_{timestamp}.json"
# → traffic_20250623_142301.json
```

**Concepts:** `datetime.now()`, `strftime` format codes, `os.path.splitext`, f-strings.

---

### 7. Input Validation & Custom Errors

`validate_args()` raises Python built-in exceptions with descriptive messages, following the "fail fast" principle.

```python
if not args.file:
    raise ValueError("PCAP mode requires --file")

if not os.path.exists(args.file):
    raise FileNotFoundError("PCAP file not found")
```

**Concepts:** `ValueError`, `FileNotFoundError`, defensive programming, separating validation logic from business logic.

---

### 8. Third-Party Library — Scapy

Scapy is the core packet manipulation library. Key APIs used:

```python
from scapy.all import sniff, rdpcap, get_if_list, conf, IP, TCP, UDP

sniff(iface="eth0", prn=callback, filter="tcp", store=False)  # live
packets = rdpcap("capture.pcap")                               # offline
packet.haslayer(TCP)                                           # layer check
packet[IP].src                                                 # field access
```

**Concepts:** callback-driven packet processing, BPF filters, layer-based packet model.

---

## ⚙️ Requirements

```
Python 3.8+
scapy
```

Install dependencies:

```bash
pip install scapy
```

> **Linux / macOS:** Live capture requires `sudo` (raw socket access).  
> **Windows:** Install [Npcap](https://npcap.com/) for Scapy to capture on Windows.

---

## 🚀 Usage

### List available network interfaces

```bash
python sniffer.py --list-ifaces
```

### Live capture (all traffic)

```bash
sudo python sniffer.py --mode live --iface eth0
```

### Live capture (TCP only, custom log file)

```bash
sudo python sniffer.py --mode live --iface eth0 --filter tcp --log session.log
```

### Analyse a PCAP file

```bash
python sniffer.py --mode pcap --file capture.pcap --filter udp
```

### Full argument reference

```
--mode          live | pcap          Capture mode (required)
--iface         <interface>          Network interface (live mode only)
--file          <path>               PCAP file path (pcap mode only)
--filter        tcp | udp | all      Protocol filter (default: all)
--log           <filename>           Base name for the log file (default: traffic.log)
--list-ifaces                        Print available interfaces and exit
```

---

## 📁 Output Files

Each run creates a **timestamped JSONL log**:

```
traffic_20250623_142301.json
```

Each line is one packet:

```json
{"timestamp": 1750694581.42, "src_ip": "192.168.1.10", "dst_ip": "93.184.216.34", "protocol": "TCP", "src_port": 54231, "dst_port": 443}
{"timestamp": 1750694581.89, "src_ip": "192.168.1.1",  "dst_ip": "192.168.1.10",  "protocol": "UDP", "src_port": 53,    "dst_port": 5353}
```

---

## 🚨 Port Scan Detection Logic

The `TrafficTracker` class watches for **horizontal port scanning** — a single source IP probing many destination ports in a short window:

```
Threshold : ≥ 10 unique destination ports
Window    : within any 30-second rolling period
Action    : print ALERT to console, log alert event, reset counters for that IP
```

> The rolling window is maintained by pruning old timestamps on every packet update, keeping memory use constant regardless of capture duration.

---

## 🗂️ Project Structure

```
python-cybersecurity-learning-toolkit/
├── module_06_network_sniffer/
│   ├── sniffer.py          ← main tool
│   ├── README.md           ← this file
│   └── samples/
│       └── example.pcap    ← sample PCAP for testing (optional)
```

---
## 📚 Key Concepts Checklist

- [x] `argparse` — CLI design with flags, choices, and defaults
- [x] OOP (`class`, `__init__`, instance methods, class constants)
- [x] `collections.defaultdict` — auto-initialised dictionaries
- [x] Closures & higher-order functions (factory/callback pattern)
- [x] File I/O — JSONL logging with `json.dumps` / `json.loads`
- [x] `datetime.strftime` — timestamped filenames
- [x] Input validation with built-in exceptions
- [x] Third-party library integration (Scapy)
- [x] BPF packet filters
- [x] Rolling time-window anomaly detection

---

*Part of the [python-cybersecurity-learning-toolkit](https://github.com/PASAN121/python-cybersecurity-learning-toolkit) · Built for learning, not production use.*
