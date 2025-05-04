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
PROGRAM_NAME = "Subtitle Generator"
SUPPORTED_EXTENSIONS = [".srt"]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

input_foldername = 'input'
output_foldername = 'output'
config_foldername = 'config'
log_foldername = 'logs'
log_filename = f"{timestamp}_log.log"

path_script = os.path.realpath(__file__)
path_project = os.path.dirname(os.path.dirname(path_script))
path_input = os.path.join(path_project, input_foldername)
path_output = os.path.join(path_project, output_foldername)
path_config = os.path.join(path_project, config_foldername, 'config.yaml')
path_log = os.path.join(path_project, log_foldername)
path_log_file = os.path.join(path_log, log_filename)

os.makedirs(path_input, exist_ok=True)
os.makedirs(path_output, exist_ok=True)
os.makedirs(path_log, exist_ok=True)

log_format = f"{PROGRAM_NAME}: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)
file_handler = logging.FileHandler(path_log_file)
file_handler.setFormatter(logging.Formatter(log_format))
logging.getLogger().addHandler(file_handler)

logging.info("Starting Subtitle Generator")
logging.info(f"Input folder: {path_input}")

# reading config
try:
    with open(path_config, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
except Exception as e:
    logging.error(f"Failed to load config.yaml: {e}")
    sys.exit(1)

input_lang = config.get("input_language", "auto")
output_lang = config.get("output_languages", [])

logging.info(f"Input language: {input_lang}")
logging.info(f"Output languages: {output_lang}")

#argos check
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

# mapping input files
input_files = [
    f for f in os.listdir(path_input)
    if os.path.splitext(f)[1].lower() in SUPPORTED_EXTENSIONS
]

if not input_files:
    logging.warning("No input valid files ({SUPPORTED_EXTENSIONS}) found in input folder.")
    sys.exit(0)

logging.info(f"Found {len(input_files)} subtitle files:")


# looping input files

for input_file in input_files:
    logging.info(f" - {input_file}")
    input_file_path = os.path.join(path_input, input_file)
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        logging.error(f"Failed to read file {input_file}: {e}")
        continue

    # checking source language
    # detecting language in case of auto as input
    if input_lang == "auto":
        try:
            text_lines = [
                line.strip() for line in lines
                if line.strip() and not line.strip().isdigit() and '-->' not in line
            ]
            sample_text = ' '.join(text_lines[:5])
            from_lang = langdetect.detect(sample_text)
            logging.info(f"[{input_lang}] Detected language: {from_lang}")
        except Exception as e:
            logging.error(f"[{input_lang}] Failed to detect language: {e}")
            continue
    else:
        from_lang = input_lang
        logging.info(f"[{input_file}] Using configured input language: {from_lang}")

    # Loop through output languages
    for to_lang in output_lang:

        output_filename = os.path.splitext(input_file)[0] + f"_{to_lang}.srt"
        output_path = os.path.join(path_output, output_filename)

        if from_lang == to_lang:
            logging.info(f"[{input_file}] Skipping '{to_lang}' (same as input language)")
            continue
        
        package_to_install = next(
            filter(
                lambda x: x.from_code == from_lang and x.to_code == to_lang, available_packages
            ), None
        )

        if not package_to_install:
            logging.warning(f"[{input_file}] No valid translation path for {from_lang} -> {to_lang}")
            continue
        try:
            logging.info(f"[{input_file}] Installing translation model: {from_lang} -> {to_lang}")
            argostranslate.package.install_from_path(package_to_install.download())
        except Exception as e:
            logging.error(f"[{input_file}] Failed to install model {from_lang} -> {to_lang}: {e}")
            continue


        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang_obj = list(filter(lambda x: x.code == from_lang, installed_languages))[0]
        to_lang_obj = list(filter(lambda x: x.code == to_lang, installed_languages))[0]

        translator = from_lang_obj.get_translation(to_lang_obj)

        logging.info(f"[{input_file}] Starting translation: {from_lang} -> {to_lang}")

        try:
            with open(output_path, 'w', encoding='utf-8') as out_file:
                for line in lines:
                    if line.strip().isdigit() or '-->' in line or not line.strip():
                        out_file.write(line)
                    else:
                        translated = translator.translate(line.strip())
                        out_file.write(translated + '\n')
            logging.info(f"[{input_file}] Translated file saved: {output_filename}")
        except Exception as e:
            logging.error(f"[{input_file}] Failed to write translated file '{output_filename}': {e}")
        