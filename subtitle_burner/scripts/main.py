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

    # Load config
    try:
        with open(path_config, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load config.yaml: {e}")
        sys.exit(1)

    # Get parameters
    subtitle_file = config.get("subtitle_file", "subtitles.srt")
    output_suffix = config.get("output_suffix", "_with_subs")

    input_video_path = os.path.join(path_input, "video.mp4")
    subtitle_path = os.path.join(path_input, subtitle_file)
    output_video_path = os.path.join(path_output, f"video{output_suffix}.mp4")

    try:
        os.makedirs(path_output, exist_ok=True)
        ffmpeg.input(input_video_path).output(output_video_path, vf=f"subtitles={subtitle_path}").run()
        logging.info(f"Successfully burned subtitles into video.")
        logging.info(f"Output saved to {output_video_path}")
    except Exception as e:
        logging.error(f"Error during ffmpeg processing: {e}")
        sys.exit(1)

    logging.info("Subtitle Burning Process Completed")

if __name__ == "__main__":
    main()
