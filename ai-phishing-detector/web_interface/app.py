from flask import Flask, render_template, request
import sys
import os
import pandas as pd
import joblib

# Add project root to path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from features.url_features import extract_url_features
from features.html_features import extract_html_features
from utils.fetch_html import fetch_html

app = Flask(__name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../model/saved_models.pkl")

# Load model once at startup
try:
    model = joblib.load(MODEL_PATH)
    print(f"[+] Model loaded successfully from {MODEL_PATH}")
except FileNotFoundError:
    print("[-] Model not found! Please run train.py first.")
    model = None

def get_prediction(url):
    logs = []
    logs.append(f"[*] Analyzing URL: {url}")
    
    if not model:
        logs.append("[-] Model not found! Please run train.py first.")
        return "ERROR", 0, 0, logs

    # 1. Feature Extraction (Copying logic from detect.py)
    features = extract_url_features(url)
    
    html = fetch_html(url)
    if html:
        logs.append(f"[+] Successfully fetched HTML for {url}")
        features.update(extract_html_features(html, url))
    else:
        logs.append(f"[-] Failed to fetch HTML for {url} (or not found). Using default safe values.")
        # Defaults
        features.update({
            "has_password_field": 0,
            "num_forms": 0,
            "external_form_action": 0,
            "hidden_inputs": 0,
            "num_iframes": 0,
            "suspicious_keywords": 0,
            "has_suspicious_js": 0,
            "external_resources_ratio": 0.0,
            "title_has_login": 0
        })

    logs.append(f"[DEBUG] Extracted Features: {features}")

    # 2. Prediction
    feature_df = pd.DataFrame([features])
    
    prediction = model.predict(feature_df)[0]
    phishing_prob = model.predict_proba(feature_df)[0][1]

    result = "PHISHING" if prediction == 1 else "SAFE"
    confidence = phishing_prob if prediction == 1 else (1 - phishing_prob)
    
    return result, confidence, phishing_prob, logs

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            result, conf, prob, logs = get_prediction(url)
            return render_template("index.html", 
                                   url=url, 
                                   result=result, 
                                   confidence=f"{conf:.2%}", 
                                   probability=f"{prob:.2%}",
                                   logs=logs)
    
    return render_template("index.html")

if __name__ == "__main__":
    print("[*] Starting Web Interface on http://localhost:4444")
    # Setting use_reloader=False helps prevent double-binding of the port 
    # which is often the cause of "address already in use" on macOS.
    app.run(debug=True, port=4444, host="0.0.0.0", use_reloader=False)