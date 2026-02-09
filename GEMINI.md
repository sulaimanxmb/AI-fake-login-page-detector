# Project Context: AI Phishing Detector (Complete)

## Project Overview
This project is a Python-based Machine Learning application designed to detect phishing attempts by analyzing both URL structures and HTML source code. It includes a training pipeline, a real-time inference script, a Flask-based web interface, and high-fidelity phishing simulations for testing.

## Directory Structure
- **`ai-phishing-detector/`**: Core application.
    - **`data/`**: Raw and processed datasets.
    - **`features/`**: Extraction logic for `url_features.py` and `html_features.py`.
    - **`model/`**: Training logic and saved `.pkl` model artifacts.
    - **`web_interface/`**: Flask application (`app.py`) and UI templates.
    - **`utils/`**: Helper modules for fetching HTML and data processing.
    - **`Dockerfile` & `docker-entrypoint.sh`**: Containerization setup.
- **`fake-google-login/`**: A high-fidelity phishing simulation on Port 8080.
- **`real-google-login/`**: A legitimate-looking login simulation on Port 8081 (for testing false positives).

## Feature Engineering
The model analyzes several "red flags":
- **URL Features:** IP-based URLs, long paths, and suspicious keywords (login, verify, etc.).
- **HTML Features:** 
    - Presence of password fields.
    - Form actions pointing to external domains.
    - Ratio of external assets (images/scripts) vs. local ones.
    - Hidden inputs and IFrames.
    - Obfuscated JavaScript (`eval`, `unescape`).
    - Page title and text keywords.

## Machine Learning
- **Algorithm:** Random Forest Classifier.
- **Training:** Automated via `train.py`.
- **Inference:** Probability-based scoring to determine "Safe" vs. "Phishing".

## Running the Project

### Local Execution
1. **Train:** `cd ai-phishing-detector && .venv/bin/python3 train.py`
2. **Web App:** `.venv/bin/python3 web_interface/app.py` (Runs on Port 8081)
3. **CLI Detect:** `.venv/bin/python3 detect.py <URL>`

### Phishing Simulation
1. **Start Fake Site:** `cd fake-google-login && python3 server.py` (Runs on Port 8080)
2. **Analyze via Detector:** Navigate to the Web App and enter `http://localhost:8080`.

### Docker
1. **Build:** `docker build -t phishing-detector ./ai-phishing-detector`
2. **Run:** `docker run -p 8081:8081 phishing-detector`

## Development Status
The project is fully functional with automated training on startup, visual/source-code based detection, and a professional web UI.