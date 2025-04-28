#!/bin/bash
# setup.sh - Quick setup for MinerU Lambda Extraction
set -e

cd "$(dirname "$0")/app"

echo "[1/3] Installing Python dependencies..."
pip install -r requirements.txt

echo "[2/3] Downloading models and patching config..."
python setup_magic_pdf.py

echo "[3/3] Setup complete."
