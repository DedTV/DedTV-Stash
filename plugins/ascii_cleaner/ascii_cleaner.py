import sys
import json
import os
import re

# --- CONFIGURATION ---
# This can be overridden by the task or left as a default
ROOT_PATH = r"F:\"
# ---------------------

def clean_text(text):
    # Strip non-ASCII (Emojis, special symbols)
    cleaned = re.sub(r'[^\x00-\x7F]+', '', text)
    # Clean up double spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # Trim leading/trailing spaces and dots
    return cleaned.strip(" .")

def process_files(root_path, dry_run):
    print(f"--- Starting Scan of {root_path} (Dry Run: {dry_run}) ---")
    
    for root, dirs, files in os.walk(root_path):
        for name in files:
            # Check if name contains non-ASCII
            if not all(ord(c) < 128 for c in name):
                new_name = clean_text(name)
                
                # Ensure the new name isn't empty
                if new_name and new_name != name:
                    old_path = os.path.join(root, name)
                    new_path = os.path.join(root, new_name)

                    if dry_run:
                        print(f"[DRY RUN] Would rename: '{name}' -> '{new_name}'")
                    else:
                        try:
                            # Handle potential name collisions
                            if os.path.exists(new_path):
                                print(f"[SKIP] Destination exists: {new_name}")
                                continue
                                
                            os.rename(old_path, new_path)
                            print(f"[SUCCESS] Renamed: {new_name}")
                        except Exception as e:
                            print(f"[ERROR] Failed on {name}: {str(e)}", file=sys.stderr)

def main():
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        input_data = {}

    args = input_data.get("args", {})
    mode = args.get("mode")
    
    # Check dryRun setting from Stash UI Task args
    dry_run = args.get("dryRun", True)

    if mode == "bulk":
        process_files(ROOT_PATH, dry_run)
        if not dry_run:
            print("\nIMPORTANT: Please run a Library Scan in Stash to update the database.")
    else:
        print("Plugin loaded. Run via the Tasks menu.")

if __name__ == "__main__":
    main()
