# AI Phishing Detector

An AI-powered tool to detect phishing websites by analyzing URL structure and HTML source code features. This project uses a Random Forest classifier to distinguish between safe and malicious sites.

## 🚀 Quick Start (Re-creating from Scratch)

If you are setting this up on a new machine after a few months, follow these exact steps.

### Prerequisites
*   **Python 3.11+** installed.
*   **Docker** (optional, for containerized run).

### 1. Installation
Clone the repository and navigate to the project folder:
```bash
cd ai-phishing-detector
```

Create a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Training the Model
You must train the model at least once before using it. This will create the `model/saved_models.pkl` file.

```bash
python3 train.py
```
*Output should show "Model saved to model/saved_models.pkl".*

### 3. Running the Web Interface
Start the local web server to use the graphical detector:

```bash
python3 web_interface/app.py
```
*Access the tool at: http://localhost:8081*

### 4. Running CLI Detection
To check a specific URL from the command line:

```bash
python3 detect.py "http://google.com"
```

---

## 🧪 Testing with Simulations

To verify the detector works, you can run the included simulation environments.

### Fake Google Login (Phishing)
1.  Open a new terminal.
2.  `cd ../fake-google-login`
3.  `python3 server.py` (Runs on Port 8080)
4.  Test URL: `http://localhost:8080` -> **Should be RED (Phishing)**

### Real Google Login (Safe Simulation)
1.  Open a new terminal.
2.  `cd ../real-google-login`
3.  `python3 server.py` (Runs on Port 8081)
4.  Test URL: `http://localhost:8081` -> **Should be GREEN (Safe)** (Ensure port 8081 is free first!)

---

## 🐳 Docker Usage (Easiest Method)

If you don't want to install Python manually:

1.  **Build:**
    ```bash
    docker build -t phishing-detector .
    ```

2.  **Run:**
    ```bash
    docker run -p 8081:8081 phishing-detector
    ```
    *This automatically handles training and starts the website.*

## 🛠 Project Structure
*   `data/`: CSV datasets for training.
*   `features/`: Logic for extracting URL and HTML features.
*   `model/`: Training scripts and saved models.
*   `web_interface/`: Flask web application.
