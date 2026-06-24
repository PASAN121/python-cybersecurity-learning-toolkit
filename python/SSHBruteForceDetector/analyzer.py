import re
from collections import defaultdict # dict with auto-initialized default values

def analyze_log(log_data, threshold=5):
    failed_attempts = defaultdict(int) # counts total failed attempts per IP
    successful_logins = defaultdict(list) # stores successful login timestamps per IP
    failed_details = defaultdict(list) # stores failed login timestamps per IP

    pattern = re.compile(
        r"(\w{3}\s+\d+\s+\d+:\d+:\d+).*?(Failed|Accepted) password for \S+ from (\d+\.\d+\.\d+\.\d+)"
    )

     # iterate over every line in the log file
    for line in log_data:
        match = pattern.search(line) # search anywhere in line, not just start
        if not match:
            continue  # skip lines that don't match (cron jobs, reboots, etc.)

        timestamp = match.group(1)  # "Jun 15 03:22:11"
        event = match.group(2)      # "Failed" or "Accepted" 
        ip = match.group(3)         # "192.168.1.100"

        if event == "Failed":
            failed_attempts[ip] += 1 # increment failure count
            failed_details[ip].append(timestamp) # record when it happened
        elif event == "Accepted":
            successful_logins[ip].append(timestamp)# record successful login

    # dict comprehension — runs AFTER loop, filters IPs that hit the threshold
    # this is what gets passed to report.py
    
    flagged_ips = {
        ip: count
        for ip, count in failed_attempts.items()
        if count >= threshold  # threshold comes from main.py CLI arg
    }

    