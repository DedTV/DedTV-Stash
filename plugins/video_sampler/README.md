# Stash Video Sampler

A powerful automation plugin for [Stash](https://github.com/stashapp/stash) that generates high-speed video previews/samples from your existing library using FFmpeg.

Instead of manually creating clips, this plugin automatically calculates timestamps based on the total duration of a scene and extracts three 10-second segments to give you a comprehensive "at-a-glance" look at your media.

## Features

* **Smart Sampling:** Automatically calculates extraction points at **50%**, **75%**, and **90%** of the video's total runtime.
* **Lossless Extraction:** Uses FFmpeg's `-c copy` (stream copying) technology. This creates samples in seconds without re-encoding, preserving the original quality while using almost zero CPU.
* **Database Integration:** Direct integration with the Stash API. It pulls file paths directly from your database, supporting libraries spread across multiple drives or complex folder structures.
* **Targeted Tasks:**
* **Rated:** Only process your 5-star favorites.
* **Tagged:** Target a specific "queue" using a custom Stash tag (e.g., "To Sample").
* **All:** Perform a bulk operation on your entire collection.


* **Safety Checks:** Automatically verifies if a video is long enough (at least 20 seconds) before attempting to sample, preventing errors on short clips.

## How It Works

1. **Probe:** The script uses `ffprobe` to determine the exact millisecond duration of the target file.
2. **Calculate:** It generates three specific timestamps (Midpoint, Late-mid, and Finale).
3. **Extract:** It calls `ffmpeg` to "cut" 10-second segments starting at those timestamps.
4. **Output:** The resulting files are saved to your designated `TEMP` folder with a naming convention of `Filename-sample (1).mp4`.

## Installation

### 1. Requirements

* **FFmpeg:** You must have `ffmpeg` and `ffprobe` installed on your system.
* **Python Libraries:**
```bash
pip install stashapp-tools

```



### 2. Setup

1. Create a folder named `video_sampler` in your Stash `plugins` directory.
2. Place `video_sampler.py` and `video_sampler.yml` inside.
3. Edit the `CONFIGURATION` section at the top of `video_sampler.py` to match your FFmpeg paths and desired output directory:
```python
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\ffmpeg\bin\ffprobe.exe"
OUTPUT_DIR = r"F:\Temp"

```



## Usage

1. Go to **Settings > Plugins** in Stash and click **Reload Plugins**.
2. Navigate to the **Tasks** section of the Video Sampler plugin.
3. Click **Run** on your desired mode (Rated, Tagged, or All).
4. View real-time progress in the Stash **Logs** tab.

