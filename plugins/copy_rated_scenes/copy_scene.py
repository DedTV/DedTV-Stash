import sys
import json
import shutil
import os
from stashapi.stashapp import StashInterface

# --- CONFIGURATION ---
COPY_DESTINATION = r"F:\Faves" 
# ---------------------

def copy_file(scene, destination):
    files = scene.get("files", [])
    if not files:
        return False
    
    source_path = files[0].get("path")
    file_name = os.path.basename(source_path)
    dest_path = os.path.join(destination, file_name)

    if not os.path.exists(destination):
        os.makedirs(destination)

    if not os.path.exists(dest_path):
        try:
            shutil.copy2(source_path, dest_path)
            print(f"Copied: {file_name}")
            return True
        except Exception as e:
            print(f"Error copying {file_name}: {e}", file=sys.stderr)
    return False

def main():
    # Load the JSON input from Stash
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        return

    stash = StashInterface({})
    
    # Check if we are running in "bulk" mode from the Task
    # defaultArgs are passed inside input_data['args']
    args = input_data.get("args", {})
    mode = args.get("mode")

    if mode == "bulk":
        print("Starting bulk copy of 5-star scenes...")
        # Find all scenes with a 5-star rating (rating 100)
        scenes = stash.find_scenes(f={
            "rating100": {"value": 100, "modifier": "EQUALS"}
        })
        
        count = 0
        for scene in scenes:
            if copy_file(scene, COPY_DESTINATION):
                count += 1
        print(f"Bulk process complete. Copied {count} files.")

    else:
        # Handle Hook (Triggered by Scene.Update.Post)
        # The scene ID is usually in input_data['args']['id'] or ['hookContext']['id']
        scene_id = args.get("id")
        if scene_id:
            scene = stash.find_scene(scene_id)
            if scene and (scene.get("rating100") == 100 or scene.get("rating") == 5):
                copy_file(scene, COPY_DESTINATION)

if __name__ == "__main__":
    main()