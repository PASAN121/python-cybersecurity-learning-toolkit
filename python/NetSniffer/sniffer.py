import argparse
import os


def get_args():
    parser = argparse.ArgumentParser(description="Scapy Network sniffer tool")
    
    parser.add_argument(
        "--mode",required=True, choices=["live","pcap"], help= "Sniff mode: live capture or pcap analysis"
    )
    
    parser.add_argument(
        "--iface",help="Network interface (only for live mode)"
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

    return parser.parse_args()   



 

def validate_args(args):

    # LIVE MODE
    if args.mode == "live":
        if not args.iface:
            raise ValueError("Live mode requires --iface")

        if args.file:
            print("[WARN] --file ignored in live mode")


    # PCAP MODE
    elif args.mode == "pcap":

        if not args.file:
            raise ValueError("PCAP mode requires --file")

        #  check file exists
        if not os.path.exists(args.file):
            raise FileNotFoundError("PCAP file not found")

        #  basic extension check
        if not args.file.endswith((".pcap", ".pcapng")):
            raise ValueError("Invalid file type. Must be .pcap or .pcapng")

        if args.iface:
            print("[WARN] --iface ignored in pcap mode")
        