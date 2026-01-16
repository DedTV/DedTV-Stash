import sys
import json
from titlecase import titlecase
from stashapi.stashapp import StashInterface

def abbreviations_callback(word, all_caps):
    # A list of words to always keep in uppercase
    custom_abbreviations = ['USA', 'UK', 'FBI', 'CIA', 'CGI', 'DP']
    if word.upper() in custom_abbreviations:
        return word.upper()
    return None

def process_titles(stash):
    print("Fetching scenes from Stash...")
    # Get all scenes (ID and Title only to keep it fast)
    scenes = stash.find_scenes(get_all=True)
    
    total_scenes = len(scenes)
    updated_count = 0

    for index, scene in enumerate(scenes):
        scene_id = scene.get('id')
        original_title = scene.get('title')

        if not original_title:
            continue

        # Apply your titlecase logic
        corrected_title = titlecase(original_title, callback=abbreviations_callback)

        if original_title != corrected_title:
            # Update the scene via the API
            stash.update_scene({
                'id': scene_id,
                'title': corrected_title
            })
            updated_count += 1
            print(f"[{index+1}/{total_scenes}] Updated: {corrected_title}")

        if (index + 1) % 50 == 0:
            print(f"Processed {index + 1} scenes...")

    print(f"\nFinished! Updated {updated_count} titles.")

def main():
    # Read the input from Stash
    try:
        input_data = json.load(sys.stdin)
    except Exception:
        input_data = {}

    # Initialize Stash Interface
    # It automatically detects your Stash instance if running on the same machine
    stash = StashInterface(input_data.get("server_connection", {}))

    # Check if we were triggered by the Task button
    args = input_data.get("args", {})
    if args.get("mode") == "bulk":
        process_titles(stash)
    else:
        print("No task mode specified. Manual execution required.")

if __name__ == "__main__":
    main()
