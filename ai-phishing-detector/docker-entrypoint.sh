#!/bin/bash
set -e

MODEL_FILE="model/saved_models.pkl"

echo "[*] Container started."

# Start the phishing simulation servers in the background
echo "[*] Starting Phishing Simulation Servers for testing..."
python3 fake-login-pages/multi_server.py &

# Wait a moment for servers to bind to ports
sleep 1

# Start the Web Interface
echo "[*] Starting Web Interface on port 4444..."
python3 ai-phishing-detector/web_interface/app.py