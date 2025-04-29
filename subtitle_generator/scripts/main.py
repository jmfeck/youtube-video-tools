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
import whisper  # OpenAI's Whisper library

# Program metadata
PROGRAM_NAME = "Subtitle Generator"

# Supported video extensions (hardcoded)
SUPPORTED_EXTENSIONS = [".mp4", ".mkv", ".avi"]

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
    model_size = config.get("model_size", "small")  # tiny, base, small, medium, large

    try:
        os.makedirs(path_output, exist_ok=True)
        logging.info(f"Loading Whisper model '{model_size}'...")
        model = whisper.load_model(model_size)

        # List all video files
        video_files = [
            f for f in os.listdir(path_input)
            if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
        ]

        if not video_files:
            logging.warning("No supported video files found in input folder.")
            sys.exit(0)

        # Count video names (without extension)
        video_name_counts = {}
        for video_file in video_files:
            video_name, _ = os.path.splitext(video_file)
            video_name_counts[video_name] = video_name_counts.get(video_name, 0) + 1

        # Process each video
        for video_file in video_files:
            input_video_path = os.path.join(path_input, video_file)
            video_name, video_ext = os.path.splitext(video_file)
            video_ext_clean = video_ext.replace(".", "").lower()

            # Decide subtitle filename
            if video_name_counts[video_name] > 1:
                output_srt_filename = f"{video_name}_{video_ext_clean}.srt"
            else:
                output_srt_filename = f"{video_name}.srt"

            output_srt_path = os.path.join(path_output, output_srt_filename)

            logging.info(f"Processing {video_file}...")

            try:
                result = model.transcribe(input_video_path)

                with open(output_srt_path, "w", encoding="utf-8") as srt_file:
                    for idx, segment in enumerate(result["segments"]):
                        start = segment["start"]
                        end = segment["end"]
                        text = segment["text"].strip()

                        start_timestamp = format_timestamp(start)
                        end_timestamp = format_timestamp(end)

                        srt_file.write(f"{idx+1}\n")
                        srt_file.write(f"{start_timestamp} --> {end_timestamp}\n")
                        srt_file.write(f"{text}\n\n")

                logging.info(f"Subtitles generated: {output_srt_filename}")
            except Exception as e:
                logging.error(f"Failed to process {video_file}: {e}")

    except Exception as e:
        logging.error(f"General error: {e}")
        sys.exit(1)

    logging.info("Subtitle Generation Completed")

def format_timestamp(seconds: float) -> str:
    """Format seconds to SRT timestamp."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

if __name__ == "__main__":
    main()
