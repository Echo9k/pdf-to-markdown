"""
setup_magic_pdf.py
Handles model download and config file creation/patching for magic-pdf.
Call this script during Docker build or Lambda init.
"""
import os
import json
import subprocess
import sys
import urllib.request

CONFIG_PATH = os.environ.get('MAGIC_PDF_CONFIG_PATH', 'magic-pdf.json')
MODEL_SCRIPT_URL = 'https://github.com/opendatalab/MinerU/raw/dev/scripts/download_models_hf.py'
MODEL_SCRIPT_LOCAL = 'download_models_hf.py'


def download_models():
    """Download model script and run it if models are not present."""
    if not os.path.exists(MODEL_SCRIPT_LOCAL):
        try:
            print(f"Downloading {MODEL_SCRIPT_URL} ...")
            urllib.request.urlretrieve(MODEL_SCRIPT_URL, MODEL_SCRIPT_LOCAL)
        except Exception as e:
            print(f"Failed to download model script: {e}")
            sys.exit(1)
    try:
        subprocess.run([sys.executable, MODEL_SCRIPT_LOCAL], check=True)
    except Exception as e:
        print(f"Failed to run model script: {e}")
        sys.exit(1)


def patch_config():
    """Patch or create magic-pdf.json with device mode and LLM API key."""
    config = {
        "device-mode": os.environ.get('DEVICE_MODE', 'cpu'),
        "llm-aided-config": {
            "title_aided": {
                "enable": False,
                "api_key": ""
            }
        }
    }
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            try:
                config.update(json.load(f))
            except Exception:
                pass
    # Patch device mode
    config['device-mode'] = os.environ.get('DEVICE_MODE', config.get('device-mode', 'cpu'))
    # Patch LLM API key if present
    api_key = os.environ.get('LLM_API_KEY')
    if api_key:
        config.setdefault('llm-aided-config', {}).setdefault('title_aided', {})['api_key'] = api_key
        config['llm-aided-config']['title_aided']['enable'] = True
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"magic-pdf.json written to {CONFIG_PATH}")


def main():
    print("--- Downloading models (if needed) ---")
    download_models()
    print("--- Patching config ---")
    patch_config()
    print("--- Setup complete ---")

if __name__ == "__main__":
    main()
