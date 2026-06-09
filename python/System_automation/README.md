# 🗂️ File Organizer CLI

A lightweight Python command-line tool that automatically scans a messy folder and sorts files into categorized subdirectories — with full timestamped logging.

Built as a portfolio project to demonstrate practical Python automation: argument parsing, file system operations, and structured logging.

---

## ✨ Features

- **Folder scanning** — recursively lists all files in a target directory, skipping subdirectories
- **Extension-based categorization** — maps file types to `images`, `documents`, `videos`, `audio`, `archives`, and `others`
- **Auto folder creation** — creates category subdirectories only when needed (`exist_ok` safe)
- **File moving** — uses `shutil.move()` for reliable cross-platform file relocation
- **Timestamped logging** — writes every action (folder creation, move, error) to `logs/organizer_log.txt`
- **CLI interface** — clean `argparse`-powered interface with a `--folder` flag

---

## 🎬 Demo

> An interactive walkthrough — folder scan → categorization → organized output.

<div align="center">
  <a href="assets/demo.html" target="_blank">
    <img src="https://img.shields.io/badge/▶%20Open%20Live%20Demo-0d1117?style=for-the-badge&logo=python&logoColor=4ade80" alt="Open Live Demo"/>
  </a>
</div>

> 💡 Open `assets/demo.html` in your browser to see the full animated demo.
> Replace with `assets/demo.gif` once you record a real screen capture.

---

## 📁 Before vs After

**Before** — a cluttered Downloads folder:

```
Downloads/
├── photo.jpg
├── report.pdf
├── song.mp3
├── video.mp4
├── screenshot.png
└── notes.docx
```

**After** — automatically organized:

```
Downloads/
├── images/
│   ├── photo.jpg
│   └── screenshot.png
├── documents/
│   ├── report.pdf
│   └── notes.docx
├── audio/
│   └── song.mp3
└── videos/
    └── video.mp4
```

---

## 🚀 How to Run

**Requirements:** Python 3.7+, no external dependencies.

```bash
# Clone the repo
git clone https://github.com/PASAN121/python-cybersecurity-learning-toolkit
cd python
cd System_automation

# Run the organizer
python file_organizer.py --folder "C:\Users\pasan\Downloads"

# Linux / macOS
python file_organizer.py --folder "/home/pasan/Downloads"
```

---

## 📋 Logs

Every action is written to `logs/organizer_log.txt` with a full timestamp. Example output:

```
[2026-06-10 14:22:01] Starting scan: C:\Users\pasan\Downloads
[2026-06-10 14:22:02] Creating folder: C:\Users\pasan\Downloads\images
[2026-06-10 14:22:02] Creating folder: C:\Users\pasan\Downloads\documents
[2026-06-10 14:22:03] Moved 'photo.jpg' to '...\images'
[2026-06-10 14:22:03] Moved 'report.pdf' to '...\documents'
[2026-06-10 14:22:04] Moved 'song.mp3' to '...\audio'
[2026-06-10 14:22:04] Moved 'video.mp4' to '...\videos'
```

Logs are appended on each run — useful for auditing what moved and when.

---

## 🏗️ Architecture

```
file_organizer.py
│
├── main()
│   ├── argparse  ──────────────────►  --folder "path"
│   │
│   ├── validate_folder()  ─────────►  checks exists + is_dir()
│   │
│   ├── scan_folder()  ─────────────►  iterdir(), skip subdirs
│   │
│   └── for each file:
│       ├── get_file_extension()  ──►  .suffix → lowercase string
│       ├── get_category()  ────────►  extension → category name
│       ├── create_category_folder() ► mkdir(exist_ok=True)
│       └── move_file_to_category() ►  shutil.move() + log_action()
│
└── log_action()  ──────────────────►  logs/ organizer_log.txt
```

---

## 🗂️ File Type Mapping

| Category     | Extensions                              |
|--------------|-----------------------------------------|
| `images`     | jpg, jpeg, png, gif, bmp, tiff          |
| `documents`  | pdf, docx, txt, xlsx, pptx              |
| `videos`     | mp4, avi, mkv, mov                      |
| `audio`      | mp3, wav, aac                           |
| `archives`   | zip, rar, tar, gz                       |
| `others`     | anything not matched above              |

---

## 🔮 Future Improvements

- [ ] `--dry-run` flag to preview actions without moving files
- [ ] `--undo` mode to restore files using the log as a manifest
- [ ] Recursive mode to organize nested folders
- [ ] Duplicate file detection before moving
- [ ] Config file (`.yaml`) for custom extension-to-category mappings
- [ ] GUI wrapper using `tkinter` or a web frontend

---

## 📄 License

MIT License — free to use, modify, and distribute.