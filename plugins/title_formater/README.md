Here is a professional `README.md` for your GitHub repository. It is designed to be clear for users and includes all necessary setup instructions.

---

# Stash Title Case Formatter

A plugin for [Stash](https://github.com/stashapp/stash) that automatically standardizes scene titles using "smart" title casing. It ensures your library looks professional by capitalizing principal words while keeping articles, conjunctions, and specific acronyms formatted correctly.

## Features

* **Smart Capitalization:** Converts `SCENE IN ALL CAPS` or `lowercase scene title` to `Scene in All Caps`.
* **Acronym Protection:** Built-in whitelist to ensure acronyms like `USA`, `FBI`, `CIA`, `CGI`, and `DP` remain in all-caps.
* **API-Driven:** Uses the Stash API via `stashapp-tools` for safe updates that reflect immediately in the UI without requiring a restart.
* **Bulk Processing:** A manual task to scan and fix your entire existing library in one click.
* **Dry-Run Safe:** Only sends update commands to Stash if the title actually needs changing, reducing overhead.

## Installation

### 1. Prerequisites

Ensure your Python environment has the required libraries installed:

```bash
pip install titlecase stashapp-tools

```

### 2. Plugin Setup

1. Navigate to your Stash `plugins` directory.
2. Create a folder named `title_formatter`.
3. Download and place `title_formatter.py` and `title_formatter.yml` into that folder.

### 3. Registering the Plugin

1. Open Stash in your browser.
2. Go to **Settings > Plugins**.
3. Click **Reload Plugins**.
4. The "Title Case Formatter" should now appear in your plugin list.

## Usage

### Bulk Update

To format your entire library at once:

1. Go to **Settings > Plugins**.
2. Find **Title Case Formatter**.
3. Click the **Run** button next to **"Format All Scene Titles"**.
4. Monitor the progress in the **Logs** tab.

## Configuration

You can customize the acronyms that stay capitalized by editing the `custom_abbreviations` list in `title_formatter.py`:

```python
def abbreviations_callback(word, all_caps):
    custom_abbreviations = ['USA', 'UK', 'FBI', 'CIA', 'CGI', 'DP', '4K', 'VR']
    if word.upper() in custom_abbreviations:
        return word.upper()
    return None

```

