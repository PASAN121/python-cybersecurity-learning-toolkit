import argparse
from pathlib import Path
import hashlib
import os
import json
from datetime import datetime

def validate_folder(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("Error: Folder does not exist")
        return None

    if not folder.is_dir():
        print("Error: Path is not a folder")
        return None

    return folder


def hash_file(file_path):
    """
    Read a file in binary chunks and return its SHA-256 hex digest.
    Chunked reading keeps memory usage flat even for very large files.
    Returns None if the file cannot be read (locked, no permission, etc).
    """
    
    sha256 = hashlib.sha256()
   
    try:
        with open(file_path,"rb") as file:
            while chunk:= file.read(8192):             #Read 8 KB at a time
                sha256.update(chunk)

        return sha256.hexdigest()
    
    except (IOError,PermissionError) as e:
        print(f"Could read the file path{file_path} error {e}")
        return None    
    


def scan_folder(folder_path):
    """
    Walk the folder recursively and return a dict of
    { relative_path: sha256_hex } for every readable file.
    Relative paths keep the baseline portable (folder can be moved).
    """
    hashes = {}
    for dirpath, dirnames, filenames in os.walk(folder_path):
        # os.walk yields (current_dir, [subdirs], [files]) at every level
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)           # Absolute path on disk
            relative_path = os.path.relpath(full_path, folder_path)  # Relative to monitored root
            file_hash = hash_file(full_path)
            if file_hash:                                          # Skip files that couldn't be read
                hashes[relative_path] = file_hash
    return hashes
 

def save_baseline(hashes, baseline_path):
    """
    Write the hash dict to a JSON file, along with a creation timestamp
    so you always know when the baseline was established.
    """
    baseline = {
        "created_at": datetime.now().isoformat(),   # e.g. "2026-06-13T14:22:05"
        "files": hashes                              # { relative_path: sha256_hex }
    }
    with open(baseline_path, "w") as f:
        json.dump(baseline, f, indent=2)             # indent=2 makes it human-readable
        
    print(f"Baseline saved: {len(hashes)} file(s) → {baseline_path}")



def load_baseline(baseline_path):
    """
    Read baseline.json and return just the 'files' dict.
    We don't need the metadata (created_at) for comparison.
    """
    with open(baseline_path, "r") as f:
        baseline = json.load(f)
    return baseline["files"]   # { relative_path: sha256_hex }


def compare_hashes(baseline,current):
    results = {"changed": [], "new": [], "deleted": []}
 
    # Check every file we found right now
    for filepath, current_hash in current.items():
        if filepath not in baseline:
            results["new"].append(filepath)                    # Didn't exist at baseline time
        elif baseline[filepath] != current_hash:
            results["changed"].append(filepath)                # Existed but content differs
 
    # Check every file that was in the baseline
    for filepath in baseline:
        if filepath not in current:
            results["deleted"].append(filepath)                # Was there before, gone now
 
    return results











def main():
    parser = argparse.ArgumentParser(description="File Integrity Monitor")

    parser.add_argument("--folder", required=True, help="Folder to scan for integrity")
    parser.add_argument("--reset",action="store_true",help="Delete the existing baseline and rebuild")

    args = parser.parse_args()

    folder = validate_folder(args.folder)

    if not folder:
        return

    baseline_path = os.path.join(args.folder, "baseline.json")
    
    # --- Reset flag: wipe the old baseline ---
    if args.reset and os.path.exists(baseline_path):
        os.remove(baseline_path)
        print("Old baseline deleted. Rebuilding...\n")
        
        # --- Mode switch ---
    if not os.path.exists(baseline_path):
        # CREATE MODE
        print(f"No baseline found. Scanning: {folder}\n")
        hashes = scan_folder(str(folder))          # str() converts Path → string for os.walk
        save_baseline(hashes, baseline_path)
        print("\n[i] Run again to detect changes.")
        

    else:
        # COMPARE MODE
        print(f"[*] Baseline found. Scanning: {folder}\n")
        baseline = load_baseline(baseline_path)
        current  = scan_folder(str(folder))
        results  = compare_hashes(baseline, current)

        total = len(results["changed"]) + len(results["new"]) + len(results["deleted"])

        if total == 0:
            print("[✓] All files intact. No changes detected.")
        else:
            print(f"[!] {total} change(s) detected:\n")
            for f in sorted(results["changed"]):
                print(f"  MODIFIED  → {f}")
            for f in sorted(results["new"]):
                print(f"  NEW       → {f}")
            for f in sorted(results["deleted"]):
                print(f"  DELETED   → {f}")

        # Show when the baseline was taken
        with open(baseline_path) as bf:
            meta = json.load(bf)
        print(f"\n[i] Baseline created: {meta.get('created_at', 'unknown')}")
        print("[i] Use --reset to rebuild the baseline.")
     
    

if __name__ == "__main__":
    main()