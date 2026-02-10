import joblib
import pandas as pd
import sys
from features.url_features import extract_url_features
from features.html_features import extract_html_features
from utils.fetch_html import fetch_html

MODEL_PATH = "model/saved_models.pkl"

def extract_all_features(url: str) -> dict:
    features = extract_url_features(url)

    html = fetch_html(url)
    if html:
        print(f"[+] Successfully fetched HTML for {url}")
        features.update(extract_html_features(html, url))
    else:
        print(f"[-] Failed to fetch HTML for {url} (or not found). Using default safe values.")
        # If HTML fetch fails, fill with safe defaults
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

    return features

def detect(url: str):
    try:
        model = joblib.load(MODEL_PATH)
    except FileNotFoundError:
        print("[-] Model not found. Please run 'python train.py' first.")
        return

    print(f"[*] Analyzing URL: {url}")
    features = extract_all_features(url)
    print(f"[DEBUG] Extracted Features: {features}")
    
    # Convert to DataFrame to match training format
    # We must ensure columns are in the same order as training. 
    # Since we use dicts, we should ideally use the same keys.
    feature_df = pd.DataFrame([features])
    
    # Ensure column order matches if possible (simple safeguard)
    # Ideally we'd save the column names during training, but for this prototype we trust the dict keys match.
    
    prediction = model.predict(feature_df)[0]
    phishing_prob = model.predict_proba(feature_df)[0][1] # Probability of being phishing (class 1)

    result = "PHISHING" if prediction == 1 else "SAFE"
    color = "\033[91m" if prediction == 1 else "\033[92m"
    reset = "\033[0m"
    
    # Calculate confidence of the specific prediction
    confidence = phishing_prob if prediction == 1 else (1 - phishing_prob)

    print(f"\nResult: {color}{result}{reset}")
    print(f"Prediction Confidence: {confidence:.2%}")
    print(f"Phishing Probability:  {phishing_prob:.2%}")
    print("-" * 30)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url_to_check = sys.argv[1]
    else:
        # Default for testing
        url_to_check = "http://localhost:8000/login.html"
        print(f"Usage: python detect.py <url>")
        print(f"No URL provided, checking default: {url_to_check}\n")

    detect(url_to_check)
