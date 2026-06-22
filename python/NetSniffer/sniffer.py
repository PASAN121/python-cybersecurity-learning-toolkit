import argparse
import os
import json
import time
from datetime import datetime
from collections import defaultdict
from scapy.all import sniff, rdpcap, get_if_list, conf, IP, TCP, UDP


# ──────────────────── CLI ARGUMENT PARSING ────────────────────

def get_args():
    parser = argparse.ArgumentParser(description="Scapy Network sniffer tool")

    parser.add_argument(
        "--mode", choices=["live", "pcap"], help="Sniff mode: live capture or pcap analysis"
    )
    parser.add_argument(
        "--iface", required=False, help="Network interface (only for live mode)"
    )
    parser.add_argument(
        "--file", help="PCAP file path (only for pcap mode)"
    )
    parser.add_argument(
        "--filter",
        default="all",
        choices=["tcp", "udp", "all"],
        help="Filter traffic type"
    )
    parser.add_argument(
        "--log",
        default="traffic.log",
        help="Output log file"
    )
    parser.add_argument(
        "--list-ifaces",
        action="store_true",
        help="List available network interfaces"
    )

    return parser.parse_args()


# ──────────────────── INPUT VALIDATION ────────────────────

def validate_args(args):

    if args.mode == "live":
        if args.file:
            print("[WARN] --file ignored in live mode")

    elif args.mode == "pcap":
        if not args.file:
            raise ValueError("PCAP mode requires --file")

        if not os.path.exists(args.file):
            raise FileNotFoundError("PCAP file not found")

        if not args.file.endswith((".pcap", ".pcapng")):
            raise ValueError("Invalid file type. Must be .pcap or .pcapng")

        if args.iface:
            print("[WARN] --iface ignored in pcap mode")


# ──────────────────── INTERFACE LISTING ────────────────────

def list_interfaces():
    print("\n[AVAILABLE NETWORK INTERFACES]\n")
    for i, iface in enumerate(get_if_list()):
        print(f"  {i}. {iface}")


# ──────────────────── BPF FILTER BUILDER ────────────────────

def get_bpf_filter(filter_type):
    if filter_type == "all":
        return None
    return filter_type


# ──────────────────── JSON LOG FILE SETUP ────────────────────

def create_log_filename(base_name):
    """Generate a unique log filename with a timestamp so each run produces a new file."""
    name, ext = os.path.splitext(base_name)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{name}_{timestamp}.json"


# ──────────────────── PACKET PARSER ────────────────────

def parse_packet(packet):
    """Extract structured data from a single packet (IP layer required)."""

    if not packet.haslayer(IP):
        return None

    packet_data = {
        "timestamp": time.time(),
        "src_ip": packet[IP].src,
        "dst_ip": packet[IP].dst,
        "protocol": "OTHER",
    }

    if packet.haslayer(TCP):
        packet_data["protocol"] = "TCP"
        packet_data["src_port"] = packet[TCP].sport
        packet_data["dst_port"] = packet[TCP].dport

    elif packet.haslayer(UDP):
        packet_data["protocol"] = "UDP"
        packet_data["src_port"] = packet[UDP].sport
        packet_data["dst_port"] = packet[UDP].dport

    return packet_data


# ──────────────────── TRAFFIC TRACKER (IN-MEMORY) ────────────────────

class TrafficTracker:
    """
    Tracks per-source-IP activity for anomaly detection.
    Stores timestamps and destination ports to detect scanning behavior.
    """

    # Thresholds for port scan detection
    PORT_THRESHOLD = 10       # number of unique destination ports
    TIME_WINDOW = 30          # seconds within which the ports must be hit

    def __init__(self):
        self.timestamps = defaultdict(list)       # {src_ip: [epoch, ...]}
        self.dst_ports = defaultdict(set)          # {src_ip: {port, ...}}
        self.alerts = []                           # collected alert events

    def update(self, packet_data):
        """Ingest a parsed packet and check for port scan behavior."""

        src_ip = packet_data["src_ip"]
        now = packet_data["timestamp"]

        self.timestamps[src_ip].append(now)

        if "dst_port" in packet_data:
            self.dst_ports[src_ip].add(packet_data["dst_port"])

        # Prune timestamps older than the detection window
        cutoff = now - self.TIME_WINDOW
        self.timestamps[src_ip] = [t for t in self.timestamps[src_ip] if t >= cutoff]

        self._check_port_scan(src_ip, now)

    def _check_port_scan(self, src_ip, now):
        """Flag a source IP if it hit too many unique ports within the time window."""

        # Only consider ports contacted within the recent time window
        recent_times = self.timestamps[src_ip]
        if len(recent_times) < self.PORT_THRESHOLD:
            return

        unique_ports = len(self.dst_ports[src_ip])
        if unique_ports >= self.PORT_THRESHOLD:
            alert = {
                "alert": "PORT_SCAN_DETECTED",
                "src_ip": src_ip,
                "unique_ports": unique_ports,
                "time_window_sec": self.TIME_WINDOW,
                "detected_at": now,
            }
            self.alerts.append(alert)

            print(f"\n[ALERT] Possible port scan from {src_ip} "
                  f"({unique_ports} unique ports in {self.TIME_WINDOW}s)")

            # Reset counters for this IP so we don't spam duplicate alerts
            self.dst_ports[src_ip].clear()
            self.timestamps[src_ip].clear()


# ──────────────────── PACKET HANDLER + LOGGER ────────────────────

def make_packet_handler(log_file, tracker):
    """
    Returns a callback that parses each packet, logs it as JSONL,
    prints a summary line, and feeds the traffic tracker.
    """

    def packet_handler(packet):

        packet_data = parse_packet(packet)
        if packet_data is None:
            return

        # Console output
        proto = packet_data["protocol"]
        src = packet_data["src_ip"]
        dst = packet_data["dst_ip"]
        sport = packet_data.get("src_port", "-")
        dport = packet_data.get("dst_port", "-")
        print(f"[{proto}] {src}:{sport} -> {dst}:{dport}")

        # Append to JSONL log (one JSON object per line)
        with open(log_file, "a") as f:
            f.write(json.dumps(packet_data) + "\n")

        # Feed the traffic tracker for anomaly detection
        tracker.update(packet_data)

    return packet_handler


# ──────────────────── LIVE SNIFF ENGINE ────────────────────

def live_sniff(args, log_file, tracker):

    if not args.iface:
        print("[INFO] No interface provided -> using default interface")
        args.iface = conf.iface

    if args.iface not in get_if_list():
        raise ValueError(
            f"Invalid interface: {args.iface}\n"
            "Run --list-ifaces to see valid options."
        )

    bpf = get_bpf_filter(args.filter)

    print(f"[INFO] Capturing on interface: {args.iface}")
    print(f"[INFO] Filter: {args.filter}")
    print(f"[INFO] Logging to: {log_file}")
    print("[INFO] Press Ctrl+C to stop capture\n")

    try:
        sniff(
            iface=args.iface,
            prn=make_packet_handler(log_file, tracker),
            filter=bpf,
            store=False,
        )
    except KeyboardInterrupt:
        print("\n[INFO] Capture stopped by user")


# ──────────────────── PCAP ANALYSIS ENGINE ────────────────────

def pcap_sniff(args, log_file, tracker):

    print(f"[INFO] Reading PCAP file: {args.file}")

    packets = rdpcap(args.file)

    bpf = get_bpf_filter(args.filter)

    print(f"[INFO] Filter: {args.filter}")
    print(f"[INFO] Logging to: {log_file}")
    print(f"[INFO] Total packets in file: {len(packets)}\n")

    handler = make_packet_handler(log_file, tracker)

    for packet in packets:
        if bpf is None or packet.haslayer(bpf.upper()):
            handler(packet)


# ──────────────────── SUMMARY REPORT ────────────────────

def print_summary(tracker, log_file):
    """Print a final summary of captured traffic and any alerts raised."""

    print("\n" + "=" * 50)
    print("  CAPTURE SUMMARY")
    print("=" * 50)

    # Count logged packets
    total_packets = 0
    protocol_counts = defaultdict(int)

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            for line in f:
                total_packets += 1
                entry = json.loads(line)
                protocol_counts[entry["protocol"]] += 1

    print(f"  Total packets logged : {total_packets}")
    for proto, count in sorted(protocol_counts.items()):
        print(f"    {proto:6s} : {count}")

    # Unique IPs that sent traffic
    unique_sources = set(tracker.timestamps.keys()) | set(tracker.dst_ports.keys())
    print(f"  Unique source IPs    : {len(unique_sources)}")

    # Alerts
    alert_count = len(tracker.alerts)
    print(f"  Alerts raised        : {alert_count}")

    if alert_count > 0:
        print("\n  [ALERT DETAILS]")
        for a in tracker.alerts:
            print(f"    - {a['src_ip']} hit {a['unique_ports']} unique ports")

    print(f"\n  Log saved to: {log_file}")
    print("=" * 50)


# ──────────────────── MAIN CONTROLLER ────────────────────

def main():

    args = get_args()

    if args.list_ifaces:
        list_interfaces()
        return

    if not args.mode:
        print("[ERROR] --mode is required (unless using --list-ifaces)")
        return

    validate_args(args)

    # Each run gets a fresh JSON log file
    log_file = create_log_filename(args.log)
    tracker = TrafficTracker()

    if args.mode == "live":
        live_sniff(args, log_file, tracker)
    elif args.mode == "pcap":
        pcap_sniff(args, log_file, tracker)

    print_summary(tracker, log_file)


if __name__ == "__main__":
    main()
