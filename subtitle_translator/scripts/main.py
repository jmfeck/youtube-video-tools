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
import langdetect
import argostranslate.package
import argostranslate.translate

# Program metadata
PROGRAM_NAME = "Subtitle Translator"
SUPPORTED_EXTENSIONS = [".srt"]

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

    logging.info("Starting Subtitle Translator")
    logging.info(f"Timestamp: {timestamp}")
    logging.info(f"Input folder: {path_input}")
    logging.info(f"Output folder: {path_output}")

    # Load config
    try:
        with open(path_config, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load config.yaml: {e}")
        sys.exit(1)

    # Get parameters
    input_lang = config.get("input_language", "auto")
    output_langs = config.get("output_languages", [])

    logging.info(f"Input language: {input_lang}")
    logging.info(f"Output languages: {output_langs}")

    # Prepare folders
    os.makedirs(path_input, exist_ok=True)
    os.makedirs(path_output, exist_ok=True)

    # Update Argos package index
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()

    # Find subtitle files
    input_files = [
        f for f in os.listdir(path_input)
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
    ]

    if not input_files:
        logging.warning(f"No supported files found in input folder: {SUPPORTED_EXTENSIONS}")
        sys.exit(0)

    for input_file in input_files:
        logging.info(f"Processing file: {input_file}")
        input_path = os.path.join(path_input, input_file)

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            logging.error(f"Failed to read file {input_file}: {e}")
            continue

        # Detect language if needed
        if input_lang == "auto":
            try:
                text_lines = [
                    line.strip() for line in lines
                    if line.strip() and not line.strip().isdigit() and '-->' not in line
                ]
                sample_text = ' '.join(text_lines[:5])
                from_lang = langdetect.detect(sample_text)
                logging.info(f"[{input_file}] Detected language: {from_lang}")
            except Exception as e:
                logging.error(f"[{input_file}] Language detection failed: {e}")
                continue
        else:
            from_lang = input_lang
            logging.info(f"[{input_file}] Using configured language: {from_lang}")

        for to_lang in output_langs:
            if from_lang == to_lang:
                logging.info(f"[{input_file}] Skipping translation to '{to_lang}' (same as input)")
                continue

            output_filename = os.path.splitext(input_file)[0] + f"_{to_lang}.srt"
            output_path = os.path.join(path_output, output_filename)

            # Install model if needed
            package = next(
                (pkg for pkg in available_packages if pkg.from_code == from_lang and pkg.to_code == to_lang),
                None
            )

            if not package:
                logging.warning(f"[{input_file}] No translation path {from_lang} -> {to_lang}")
                continue

            try:
                logging.info(f"[{input_file}] Installing model {from_lang} -> {to_lang}")
                argostranslate.package.install_from_path(package.download())
            except Exception as e:
                logging.error(f"[{input_file}] Model installation failed: {e}")
                continue

            try:
                installed_langs = argostranslate.translate.get_installed_languages()
                from_obj = next(x for x in installed_langs if x.code == from_lang)
                to_obj = next(x for x in installed_langs if x.code == to_lang)
                translator = from_obj.get_translation(to_obj)
            except Exception as e:
                logging.error(f"[{input_file}] Translator setup failed: {e}")
                continue

            # Translate and save output
            try:
                with open(output_path, 'w', encoding='utf-8') as out_f:
                    for line in lines:
                        if line.strip().isdigit() or '-->' in line or not line.strip():
                            out_f.write(line)
                        else:
                            translated = translator.translate(line.strip())
                            out_f.write(translated + '\n')
                logging.info(f"[{input_file}] Translated file saved: {output_filename}")
            except Exception as e:
                logging.error(f"[{input_file}] Failed to write output: {e}")

    logging.info("Subtitle Translation Completed")

if __name__ == "__main__":
    main()
