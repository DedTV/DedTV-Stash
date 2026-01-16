import sys
import json
import os
import subprocess
from datetime import timedelta
from stashapi.stashapp import StashInterface

# --- CONFIGURATION ---
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\ffmpeg\bin\ffprobe.exe"
OUTPUT_DIR = r"F:\Clips"
SAMPLE_DURATION = 10

# Define your sample points here as decimals (e.g., 0.25 = 25%)
# You can add as many or as few as you like.
SAMPLE_PERCENTAGES = [0.50, 0.75, 0.90]
# ---------------------

def get_video_duration(video_path):
    try:
        cmd = [
            FFPROBE_PATH, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error probing {video_path}: {e}")
        return None

def create_video_sample(input_path, output_path, start_time_seconds):
    try:
        # Format start time for FFmpeg
        start_time_formatted = str(timedelta(seconds=start_time_seconds))
        cmd = [
            FFMPEG_PATH, "-y",
            "-ss", start_time_formatted,
            "-i", input_path,
            "-t", str(SAMPLE_DURATION),
            "-c", "copy",
            output_path
        ]
        # We use capture_output=True to keep the Stash logs clean 
        # unless there is an actual error.
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except Exception as e:
        print(f"FFmpeg error on {input_path}: {e}")
        return False

def process_scenes(stash, scenes):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    total = len(scenes)
    if total == 0:
        print("No scenes found matching the criteria.")
        return

    print(f"Starting sampling for {total} scenes using percentages: {SAMPLE_PERCENTAGES}")

    for idx, scene in enumerate(scenes):
        files = scene.get("files", [])
        if not files:
            continue

        input_file_path = files[0].get("path")
        base_name = os.path.splitext(os.path.basename(input_file_path))[0]
        
        duration = get_video_duration(input_file_path)
        
        # Ensure video is long enough to support the latest sample point
        # (duration - 10 seconds to ensure the clip doesn't go past the end)
        if not duration or duration < (max(SAMPLE_PERCENTAGES) * duration) + SAMPLE_DURATION:
            print(f"Skipping {base_name}: Video too short for requested sample points.")
            continue

        print(f"[{idx+1}/{total}] Sampling: {base_name}")

        # Generate start times based on the configuration list
        for i, pct in enumerate(SAMPLE_PERCENTAGES, 1):
            start_time = duration * pct
            
            # Safety: if the percentage results in a start time too close to the end, 
            # FFmpeg might fail. We cap it at Duration - Sample Duration.
            if start_time > duration - SAMPLE_DURATION:
                start_time = duration - SAMPLE_DURATION

            output_filename = f"{base_name}-sample ({i}).mp4"
            output_file_path = os.path.join(OUTPUT_DIR, output_filename)
            
            create_video_sample(input_file_path, output_file_path, start_time)

def main():
    try:
        input_data = json.load(sys.stdin)
    except:
        input_data = {}

    stash = StashInterface(input_data.get("server_connection", {}))
    args = input_data.get("args", {})
    mode = args.get("mode")

    scenes = []

    # Use pagesize=-1 to fetch all results without pagination
    if mode == "rated":
        scenes = stash.find_scenes(f={"rating100": {"value": 100, "modifier": "EQUALS"}}, pagesize=-1)
    
    elif mode == "tag":
        target_tag = args.get("tagName")
        print(f"Searching for scenes with tag: {target_tag}")
        
        tags = stash.find_tags(f={"name": {"value": target_tag, "modifier": "EQUALS"}}, pagesize=-1)
        if tags:
            tag_id = tags[0].get("id")
            scenes = stash.find_scenes(f={"tags": {"value": [tag_id], "modifier": "INCLUDES"}}, pagesize=-1)
        else:
            print(f"Error: Tag '{target_tag}' not found in Stash.")
            return

    elif mode == "all":
        scenes = stash.find_scenes(pagesize=-1)
    
    process_scenes(stash, scenes)

if __name__ == "__main__":
    main()
