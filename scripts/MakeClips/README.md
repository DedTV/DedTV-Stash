# Video Sampling Tool (FFmpeg/Python)

This Python script automates the creation of short video previews (samples) from a collection of MP4 files. It uses **FFmpeg** to extract clips without re-encoding, ensuring the process is extremely fast and preserves the original quality.

## Key Features

* **Automated Batch Processing**: Recursively scans a source directory and all subdirectories for `.mp4` files.
* **Smart Sampling**: For every video found, the script generates three 10-second samples at specific timestamps:
* **Sample 1**: At 50% of the video's duration.
* **Sample 2**: At 75% of the video's duration.
* **Sample 3**: At 90% of the video's duration.


* **Lossless Extraction**: Uses the `-c copy` stream mapping, which avoids re-compression. This makes the process nearly instantaneous and reduces CPU load.
* **Duration Validation**: Automatically calculates video length via `ffprobe` and skips files that are too short (under 20 seconds) to ensure meaningful samples are created.
* **Configurable Limits**: Includes a built-in safety limit (defaulted to 5 files) for testing purposes before running a full library scan.

## Internal Functions

### `get_video_duration(video_path)`

Interfaces with `ffprobe` to extract the total runtime of a video file in seconds. It handles errors such as missing files or malformed metadata.

### `create_video_sample(input_path, output_path, start_time_seconds, duration_seconds=10)`

The core processing function. It converts numerical seconds into a `HH:MM:SS.ss` timestamp format and executes the FFmpeg subprocess to slice the video.

### `main()`

The orchestrator that manages directory traversal, ensures the output folder exists, enforces the file limit, and handles the naming convention for the output files: `OriginalFileName-sample (n).mp4`.

## Prerequisites

* **Python 3.x**
* **FFmpeg & FFprobe**: Must be installed on the system. The script requires the direct paths to the executables (`ffmpeg.exe` and `ffprobe.exe`) to be defined in the configuration section.
