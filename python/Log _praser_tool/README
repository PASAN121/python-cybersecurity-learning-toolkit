# SSH Log Parser

A Python tool for parsing SSH authentication logs, extracting failed and accepted login attempts, and generating attack summaries.

## Features

- Parses SSH log files for `Failed` and `Accepted` password events
- Extracts timestamp, status, username, and IP address from each entry
- Saves structured results to JSON
- Generates a summary report including top attacker IPs and targeted usernames

## Requirements

- Python 3.6+
- Standard library only (`pathlib`, `re`, `json`, `collections`)

## Usage

```bash
python log_parser.py
```

You will be prompted to enter the path to your log file:

```
Enter the path to the log file: /var/log/auth.log
```

## Output

Two files are created in an `outputs/` folder next to your log file:

| File | Description |
|---|---|
| `parsed_logs.json` | All matched log entries with timestamp, status, username, and IP |
| `summary.json` | Aggregated statistics and top attacker/target rankings |

### Example `parsed_logs.json` entry

```json
{
    "timestamp": "Jan 15 03:22:11",
    "status": "Failed",
    "username": "root",
    "ip_address": "192.168.1.105"
}
```

### Example `summary.json`

```json
{
    "total_attempts": 320,
    "failed_attempts": 315,
    "accepted_attempts": 5,
    "failed_percentage": 98.44,
    "unique_ips": 12,
    "unique_usernames": 8,
    "top_5_attacker_ips": [["192.168.1.105", 142], ["10.0.0.23", 87]],
    "top_5_targeted_users": [["root", 200], ["admin", 75]]
}
```

## Supported Log Format

The parser targets standard Linux `auth.log` / `syslog` SSH entries:

```
Jan 15 03:22:11 hostname sshd[1234]: Failed password for root from 192.168.1.105 port 54321 ssh2
Jan 15 03:25:00 hostname sshd[1234]: Accepted password for deploy from 10.0.0.5 port 22 ssh2
Jan 15 03:26:44 hostname sshd[1234]: Failed password for invalid user testuser from 203.0.113.9 port 41022 ssh2
```

> Lines that don't match this pattern are silently skipped.

## Functions

| Function | Description |
|---|---|
| `validate_file(file)` | Checks that the path exists and is a regular file |
| `read_log_file(file_path)` | Reads all lines from the log file |
| `parsed_log_data(line)` | Applies the regex pattern to a single line and returns a dict or `None` |
| `save_to_json(parsed_data, output_file)` | Serializes the list of entries to a JSON file |
| `generate_summary(parsed_data)` | Computes totals, percentages, unique counts, and top-5 rankings |