# report.py
import json # for writing structured JSON output
import os
from datetime import datetime

def generate_report(flagged_ips, failed_details, successful_logins):
     # build the report dict — this becomes the JSON file
    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_flagged_ips": len(flagged_ips),
        "threats": []
    }
     # print header
    print("\n" + "="*60)
    print("       SSH BRUTE FORCE THREAT REPORT")
    print("="*60)

    if not flagged_ips:
        print("No malicious IPs detected.")
    else:
        for ip, count in flagged_ips.items():
            # compromise indicator — IP failed AND also got a successful login
            compromised = ip in successful_logins and len(successful_logins[ip]) > 0
             # build threat entry for this IP
            threat = {
                "ip": ip,
                "failed_attempts": count,
                "first_seen": failed_details[ip][0],   # earliest timestamp
                "last_seen": failed_details[ip][-1], # latest timestamp
                "compromised": compromised,
                "successful_logins": successful_logins.get(ip, []) # safe get, [] if missing
            }

            report["threats"].append(threat) # add to report

            print(f"\n[{'COMPROMISED' if compromised else 'THREAT'}] {ip}")
            print(f"  Failed attempts : {count}")
            print(f"  First seen      : {failed_details[ip][0]}")
            print(f"  Last seen       : {failed_details[ip][-1]}")
            if compromised:
                print(f"  Successful login: {successful_logins[ip]}")

    print("\n" + "="*60 + "\n")

     # create outputs/ folder if it doesn't exist — exist_ok=True prevents error if already there
    os.makedirs("outputs", exist_ok=True)
    output_path = "outputs/ssh_threat_report.json"

     # write report dict as formatted JSON to fiLE      
    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"JSON report saved to {output_path}")