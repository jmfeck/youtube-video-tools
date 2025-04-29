# -*- coding: utf-8 -*-

# ==============================================================================
#   Author: João Manoel Feck
#   Email: joaomfeck@gmail.com
#   GitHub: https://github.com/jmfeck
# ==============================================================================

import os
import sys
import yaml
import logging
from datetime import datetime
import ffmpeg

# Program metadata
PROGRAM_NAME = "Subtitle Burner"
SUPPORTED_VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi"]

def main():
    # Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Folder names
    input_foldername = 'input'
    output_foldername = 'output'
    config_foldername = 'config'
    log_foldername = 'logs'
    log_filename = f"{timestamp}_log.log"

    # Define paths
    path_script = os.path.realpath(__file__)
    path_project = os.path.dirname(os.path.dirname(path_script))
    path_input = os.path.join(path_project, input_foldername)
    path_output = os.path.join(path_project, output_foldername)
    path_config = os.path.join(path_project, config_foldername, 'config.yaml')
    path_log_folder = os.path.join(path_project, log_foldername)
    path_log = os.path.join(path_log_folder, log_filename)

    # Set up logging
    os.makedirs(path_log_folder, exist_ok=True)
    log_format = f"{PROGRAM_NAME}: %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    file_handler = logging.FileHandler(path_log)
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)

    logging.info("Starting Process")
    logging.info(f"Timestamp: {timestamp}")
    logging.info(f"Input folder: {path_input}")
    logging.info(f"Output folder: {path_output}")

    # Load config (only output suffix needed)
    try:
        with open(path_config, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load config.yaml: {e}")
        sys.exit(1)

    output_suffix = config.get("output_suffix", "_with_subs")

    try:
        os.makedirs(path_output, exist_ok=True)

        # Get all .srt and video files
        files = os.listdir(path_input)
        video_files = [f for f in files if os.path.splitext(f)[1].lower() in SUPPORTED_VIDEO_EXTENSIONS]
        subtitle_files = {os.path.splitext(f)[0]: f for f in files if f.endswith(".srt")}

        if not video_files:
            logging.warning("No video files found.")
            sys.exit(0)

        for video_file in video_files:
            base_name, ext = os.path.splitext(video_file)
            video_path = os.path.join(path_input, video_file)

            if base_name not in subtitle_files:
                logging.warning(f"No matching subtitle found for {video_file}, skipping.")
                continue

            subtitle_file = subtitle_files[base_name]
            subtitle_path = os.path.join(path_input, subtitle_file)
            output_filename = f"{base_name}{output_suffix}.mp4"
            output_path = os.path.join(path_output, output_filename)

            logging.info(f"Burning subtitles into: {video_file}")
            try:
                subtitle_path_escaped = f'"{subtitle_path}"'
                ffmpeg.input(video_path).output(output_path, vf=f"subtitles={subtitle_path_escaped}").run()
                logging.info(f"Output saved: {output_filename}")
            except Exception as e:
                logging.error(f"Failed to process {video_file}: {e}")

    except Exception as e:
        logging.error(f"General error: {e}")
        sys.exit(1)

    logging.info("Subtitle Burning Process Completed")

if __name__ == "__main__":
    main()