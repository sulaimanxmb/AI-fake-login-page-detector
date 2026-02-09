#!/bin/bash
set -e

MODEL_FILE="model/saved_models.pkl"

echo "[*] Container started."

# Check if the model exists
if [ ! -f "$MODEL_FILE" ]; then
    echo "[-] Model artifact not found at $MODEL_FILE"
    echo "[*] Starting automatic training..."
    python3 train.py
else
    echo "[+] Found existing model at $MODEL_FILE"
fi

# Start the Web Interface
echo "[*] Starting Web Interface..."
python3 web_interface/app.py