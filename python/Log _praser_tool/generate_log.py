# generate_auth_log.py
# Creates a realistic sample auth.log file for our parser to read.
# Real auth.log files live at /var/log/auth.log on Linux/macOS systems.

import random  # For picking random values from lists

# ── Sample data pools ──────────────────────────────────────────────────────────

# A mix of attacker IPs and a "legitimate" office IP
IP_ADDRESSES = [
    "192.168.1.105",   # internal office machine
    "10.0.0.42",       # another internal machine
    "203.0.113.77",    # external attacker #1  (TEST-NET, safe for examples)
    "198.51.100.23",   # external attacker #2
    "198.51.100.99",   # external attacker #3
]

# Realistic mix of valid users, guessed names, and non-existent ones
USERNAMES = ["alice", "bob", "root", "admin", "deploy", "ftpuser", "guest"]

# sshd writes log lines with a fixed format; we mimic it here
LOG_LINES = [
    # Successful password login
    "Jun  5 14:22:01 webserver sshd[1234]: Accepted password for {user} from {ip} port {port} ssh2",
    # Successful publickey login
    "Jun  5 14:23:45 webserver sshd[1235]: Accepted publickey for {user} from {ip} port {port} ssh2",
    # Failed password attempt (wrong password for valid user)
    "Jun  5 14:25:10 webserver sshd[1236]: Failed password for {user} from {ip} port {port} ssh2",
    # Failed attempt for a user that doesn't exist on the system
    "Jun  5 14:26:33 webserver sshd[1237]: Failed password for invalid user {user} from {ip} port {port} ssh2",
    # Connection attempt that never sent credentials
    "Jun  5 14:27:00 webserver sshd[1238]: Connection closed by {ip} port {port} [preauth]",
]

# Realistic timestamps spread across one day (month day hour:min:sec)
TIMESTAMPS = [
    "Jun  1 08:14:22", "Jun  1 09:30:05", "Jun  2 11:45:17",
    "Jun  3 13:22:44", "Jun  3 15:01:33", "Jun  4 02:17:59",
    "Jun  4 03:45:12", "Jun  5 14:22:01", "Jun  5 14:23:45",
    "Jun  5 14:25:10", "Jun  5 14:26:33", "Jun  5 14:27:00",
    "Jun  6 00:01:44", "Jun  6 01:22:05", "Jun  7 18:55:30",
]

# ── Build the file ─────────────────────────────────────────────────────────────

lines = []  # We'll collect every log line here before writing

for _ in range(40):                          # Generate 40 log entries
    template = random.choice(LOG_LINES)      # Pick a random line template
    timestamp = random.choice(TIMESTAMPS)    # Pick a random timestamp
    ip = random.choice(IP_ADDRESSES)         # Pick a random source IP
    user = random.choice(USERNAMES)          # Pick a random username
    port = random.randint(1024, 65535)       # SSH source port is ephemeral (1024–65535)

    # str.format() fills in {user}, {ip}, {port} placeholders in the template.
    # We also swap out the hardcoded "Jun  5 14:22:01" prefix with our random timestamp.
    line = template.format(user=user, ip=ip, port=port)

    # Replace only the first occurrence of the fixed date with our random one.
    # This is a plain string replace — not regex — because the target is literal.
    line = line.replace("Jun  5 14:22:01", timestamp, 1)
    line = line.replace("Jun  5 14:23:45", timestamp, 1)
    line = line.replace("Jun  5 14:25:10", timestamp, 1)
    line = line.replace("Jun  5 14:26:33", timestamp, 1)
    line = line.replace("Jun  5 14:27:00", timestamp, 1)

    lines.append(line)

# Write all lines to auth.log, one per line.
# "w" mode creates the file if it doesn't exist, or overwrites it if it does.
with open("auth.log", "w") as f:
    f.write("\n".join(lines) + "\n")  # join with newlines; add a final newline at EOF

print(f"auth.log created with {len(lines)} entries.")