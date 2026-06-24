# main.py
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="SSH Brute Force Detector - Analyze auth.log for malicious IPs"
    )

    # positional argument — required, user must provide log file path
    parser.add_argument(
        "log_file",
        help="Path to the SSH log file (e.g., /var/log/auth.log)"
    )
    # optional flag — defaults to 5, user can override with --threshold 10
    parser.add_argument(
        "--threshold",
        type=int,
        default=5,
        help="Failed attempt threshold to flag an IP as malicious (default: 5)"
    )

    args = parser.parse_args() # parse sys.argv and populate args.log_file and args.threshold

    try:
        # open log file and read all lines into a list of strings
        with open(args.log_file, "r") as f:
            log_data = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {args.log_file}")
        sys.exit(1)
    # /var/log/auth.log requires root on real Linux systems
    except PermissionError:
        print(f"[ERROR] Permission denied: {args.log_file}")
        sys.exit(1)


if __name__ == "__main__":
    main() # only runs when executed directly, not when imported