# Stash Filename ASCII Cleaner

A Python-based task plugin for [Stash](https://github.com/stashapp/stash) designed to sanitize your media library by removing emojis, symbols, and non-ASCII characters from filenames.

This plugin ensures your filenames are compatible with all file systems and prevents character encoding issues in external media players or metadata scrapers.

## Features

* **Database-Targeted Scanning:** Unlike generic scripts that scan entire drives, this plugin queries your Stash database to find and rename only the files managed by your instance.
* **Smart Cleaning Logic:** * Removes non-ASCII characters (emojis, special symbols, etc.).
* Collapses multiple spaces into a single space.
* Trims leading/trailing spaces and dots.


* **Multi-File Support:** Corrects filenames for all file versions associated with a single scene.
* **Built-in Safety (Dry Run):** Includes a "Dry Run" mode by default, allowing you to preview all changes in the Stash logs before any files are actually moved.
* **Collision Prevention:** Automatically checks if a destination filename already exists to prevent accidental overwriting of media.

## How It Works

The script iterates through your Stash library, identifies filenames containing characters outside the standard ASCII range (`\x00-\x7F`), and applies a regex-based cleaning process. It uses the `os.rename` operation to perform the change on your storage device.

## Installation

1. **Prerequisites:** Ensure you have the Stash Python API library installed:
```bash
pip install stashapp-tools

```


2. **Plugin Placement:**
* Create a folder named `ascii_cleaner` in your Stash `plugins` directory.
* Place `ascii_cleaner.py` and `ascii_cleaner.yml` inside that folder.


3. **Activation:**
* Open Stash and go to **Settings > Plugins**.
* Click **Reload Plugins**.



## Usage

1. **Preview Changes:** Go to **Settings > Plugins**, find **Filename ASCII Cleaner**, and click **Run**. Check your Stash **Logs** to see the list of intended renames.
2. **Commit Changes:** Once satisfied, edit `ascii_cleaner.yml` to set `dryRun: false`.
3. **Execute:** Run the task again.
4. **Finalize:** After the script finishes, click **Scan** in your Stash Library settings to update the database with the new file paths.

