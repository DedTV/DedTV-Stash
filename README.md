# DedTV Stash Plugins Collection

A suite of automation tools and utility plugins for [Stash](https://github.com/stashapp/stash).

#### NOTE: These plugins are mostly AI generated from stand alone scripts for use with the latest Development version of Stash. They have not been fully tested and may not function on the latest Stable version or future Dev versions. **Use at your own risk!**

## 🛠 Plugins Overview

### 1. Copy 5-Star Scenes

**Function:** File Management / Favoriting
Automatically tracks your highest-rated content. When a scene is rated 5 stars, the plugin identifies the source file and copies it to a dedicated "Favorites" directory on your storage device.

* **Trigger:** Manual Task (Bulk) or Automatic Hook (on Scene Update).
* **Use Case:** Backing up your favorite scenes to a separate drive or portable device.

### 2. Title Case Formatter

**Function:** Metadata Standardization
Uses "smart" title casing logic to transform inconsistent scene titles into a professional format. It intelligently handles articles and prepositions while preserving specific acronyms.

* **Smart Logic:** Converts `SCENE IN ALL CAPS` to `Scene in All Caps`.
* **Whitelisting:** Keeps terms like `USA`, `FBI`, `CGI`, and `4K` in their proper uppercase format.
* **Integration:** Updates the Stash database directly via the API.

### 3. Filename ASCII Cleaner

**Function:** File System Hygiene
Scans filenames managed by Stash and removes "illegal" or problematic non-ASCII characters, such as emojis and special symbols.

* **Database-Targeted:** Only renames files that are currently indexed in your Stash library.
* **Safety First:** Includes a **Dry Run** mode to preview renames in the logs before any changes are committed to the disk.
* **Formatting:** Collapses multiple spaces and trims trailing dots/spaces for clean filesystem paths.

Here is the updated section for your **Video Sampler** plugin. This version explicitly details how to modify the extraction points and the specific tag used for the queuing system.

### 4. Video Sampler

**Function:** Media Processing
Automates the generation of preview clips using FFmpeg. It extracts multiple 10-second (configurable) segments from scenes to provide a comprehensive "at-a-glance" look at the content without manual seeking.

* **Configurable Extraction Points:** By default, the script takes samples at **50%, 75%, and 90%** of the video's duration.
* **Lossless Processing:** Uses stream copying (`-c copy`) for near-instant clip generation without CPU-intensive re-encoding.
* **Flexible Filtering:** Can be run against your entire library, only 5-star scenes, or scenes with a specific "To Sample" tag.

#### 🔧 Configuration Instructions

To customize how the sampler behaves, open `video_sampler.py` in a text editor and locate the `# --- CONFIGURATION ---` section:

1. **Changing Sample Points:**
Locate the `SAMPLE_PERCENTAGES` list. You can add or remove decimal values here.
* *Example for three points:* `SAMPLE_PERCENTAGES = [0.10, 0.50, 0.90]` (10%, 50%, 90%)
* *Example for five points:* `SAMPLE_PERCENTAGES = [0.20, 0.40, 0.60, 0.80, 0.95]`


2. **Configuring the "To Sample" Tag:**
The specific tag used to filter scenes is defined in the `video_sampler.yml` file under the `defaultArgs` for the **Tagged Scenes** task:
```yaml
- name: "Generate Samples for Tagged Scenes"
  defaultArgs:
    mode: "tag"
    tagName: "To Sample"  # <--- Change "To Sample" to any tag you prefer

```


*Ensure the tag exists in your Stash database before running this task.*
3. **Adjusting Clip Length:**
In `video_sampler.py`, change `SAMPLE_DURATION = 10` to your preferred length in seconds (e.g., `5` or `15`).

---

**Would you like me to add a troubleshooting section specifically for common FFmpeg path errors on Windows?**

---

## 🚀 Installation & Setup

### Requirements

All plugins require **Python 3.x** and the following libraries:

```bash
pip install stashapp-tools titlecase

```

The **Video Sampler** requires [FFmpeg](https://ffmpeg.org/) to be installed and the paths configured within the `video_sampler.py` file.

### Manual Installation

1. Download the desired plugin folder from this repository.
2. Place the folder inside your Stash `plugins/` directory.
3. Go to Stash **Settings > Plugins** and click **Reload Plugins**.

### Repository Installation

Add the following URL to your Stash Plugin Repositories to receive updates and install via the UI:
`https://dedtv.github.io/DedTV-Stash/index.yml`


## ⚠️ Important Notes

* **Renaming Safety:** After running the **Filename ASCII Cleaner**, you must run a **Scan** in Stash to update the database with the new file paths.
* **FFmpeg Paths:** Ensure you edit the `FFMPEG_PATH` and `FFPROBE_PATH` variables in `video_sampler.py` to match your local installation.
