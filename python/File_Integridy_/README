<div align="center">

```
███████╗██╗███╗   ███╗    ██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗
██╔════╝██║████╗ ████║    ██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║
█████╗  ██║██╔████╔██║    ██║ █╗ ██║███████║   ██║   ██║     ███████║
██╔══╝  ██║██║╚██╔╝██║    ██║███╗██║██╔══██║   ██║   ██║     ██╔══██║
██║     ██║██║ ╚═╝ ██║    ╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║
╚═╝     ╚═╝╚═╝     ╚═╝     ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
```

# 🛡️ File Integrity Monitor

**Track every change. Trust nothing. Know everything.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Security](https://img.shields.io/badge/Hashing-SHA--256-red?style=for-the-badge&logo=shield&logoColor=white)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)]()

*A lightweight, zero-dependency file integrity monitor that detects unauthorized modifications, new files, and deletions using SHA-256 cryptographic hashing.*

</div>

---

## 📖 Overview

FIM Watch is a command-line tool that establishes a **cryptographic baseline** of a folder and alerts you to any changes — modified files, new additions, or deletions. Perfect for monitoring config directories, source code trees, or any folder where unauthorized changes matter.

```
First run  →  builds baseline.json  (snapshot of all SHA-256 hashes)
Next runs  →  compares live state vs baseline  →  reports drift
```

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 **SHA-256 Hashing** | Cryptographically secure file fingerprinting |
| 🔄 **Recursive Scanning** | Walks entire directory trees automatically |
| 📁 **Portable Baselines** | Relative paths — move your folder freely |
| 💾 **Memory Efficient** | Chunked file reads (8 KB) for huge files |
| 🗑️ **Reset Mode** | Wipe and rebuild baseline with one flag |
| ⏱️ **Timestamped** | Know exactly when each baseline was created |
| 🎯 **Zero Dependencies** | Pure Python stdlib — nothing to install |

---

## 🚀 Quick Start

### 1. Clone & Run

```bash
git clone https://github.com/yourname/fim-watch.git
cd fim-watch
```

### 2. Create a Baseline

```bash
python fim.py --folder /path/to/your/folder
```

```
No baseline found. Scanning: /path/to/your/folder

Baseline saved: 42 file(s) → /path/to/your/folder/baseline.json

[i] Run again to detect changes.
```

### 3. Detect Changes

```bash
python fim.py --folder /path/to/your/folder
```

```
[*] Baseline found. Scanning: /path/to/your/folder

[!] 3 change(s) detected:

  MODIFIED  → config/settings.json
  NEW       → uploads/suspicious_file.exe
  DELETED   → keys/api_key.txt

[i] Baseline created: 2026-06-13T09:15:42
[i] Use --reset to rebuild the baseline.
```

### 4. Reset the Baseline

```bash
python fim.py --folder /path/to/your/folder --reset
```

---

## 🔧 Usage

```
usage: fim.py [-h] --folder FOLDER [--reset]

options:
  -h, --help       show this help message and exit
  --folder FOLDER  Folder to scan for integrity
  --reset          Delete the existing baseline and rebuild
```

---

## 📂 How It Works

```
┌─────────────────────────────────────────────────────────┐
│                    FIM Watch Flow                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   📁 Target Folder                                      │
│       │                                                 │
│       ▼                                                 │
│   🔍 os.walk() ──► every file, recursively             │
│       │                                                 │
│       ▼                                                 │
│   #️⃣  SHA-256 hash (8 KB chunks)                       │
│       │                                                 │
│       ▼                                                 │
│   baseline.json ──► { "file/path": "abc123..." }       │
│       │                                                 │
│       ▼                                                 │
│   Next run: compare live hashes vs saved               │
│       │                                                 │
│       ├──► ✅ Match  → All clear                        │
│       ├──► ⚠️  Changed → MODIFIED                       │
│       ├──► 🆕 Not in baseline → NEW                    │
│       └──► ❌ Missing from disk → DELETED               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📄 Baseline File Format

The generated `baseline.json` lives inside your monitored folder:

```json
{
  "created_at": "2026-06-13T09:15:42.123456",
  "files": {
    "config/settings.json": "e3b0c44298fc1c149afb...",
    "src/main.py":          "a665a45920422f9d417e...",
    "README.md":            "6dcd4ce23d88e2ee9568..."
  }
}
```

> **Note:** The `baseline.json` file itself is automatically excluded from change detection.

---

## 🛠️ Requirements

- Python **3.8+**
- No external packages — uses only:
  - `argparse` · `pathlib` · `hashlib` · `os` · `json` · `datetime`

---

## 🔒 Security Notes

- SHA-256 produces a **64-character hex digest** — collision resistance makes accidental false positives practically impossible.
- Store `baseline.json` somewhere **outside** the monitored folder (or in read-only storage) in high-security setups to prevent an attacker from updating the baseline alongside their changes.
- For production use, consider running on a cron schedule and piping output to a log aggregator.

---

## 🗺️ Roadmap

- [ ] `--exclude` flag to skip files/patterns
- [ ] Email / webhook alerts on change detection
- [ ] Report export (HTML / CSV)
- [ ] Watch mode (continuous polling with `--interval`)
- [ ] Colored terminal output

---

## 📜 License

MIT — do whatever you want, just don't blame us if files go missing.

---

<div align="center">

Made with 🛡️ and `hashlib`

*If your files changed and you don't know why — now you will.*

</div>