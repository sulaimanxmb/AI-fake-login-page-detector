import pandas as pd

from features.url_features import extract_url_features
from features.html_features import extract_html_features
from utils.fetch_html import fetch_html

RAW_DATA = "data/raw/phishing_urls.csv"
FEATURE_DATA = "data/processed/features.csv"

HTML_DEFAULTS = {
    "has_password_field": 0,
    "num_forms": 0,
    "external_form_action": 0,
    "hidden_inputs": 0,
    "num_iframes": 0,
    "suspicious_keywords": 0,
    "has_suspicious_js": 0,
    "external_resources_ratio": 0.0,
    "title_has_login": 0
}

def build_feature_dataset():
    df = pd.read_csv(RAW_DATA)
    rows = []

    for _, row in df.iterrows():
        url = row["url"]
        label = row["label"]

        features = extract_url_features(url)

        html = fetch_html(url)
        if html:
            features.update(extract_html_features(html, url))
        else:
            features.update(HTML_DEFAULTS)

        features["label"] = label
        rows.append(features)

    feature_df = pd.DataFrame(rows)
    feature_df.to_csv(FEATURE_DATA, index=False)

    print("[+] Feature dataset created:", FEATURE_DATA)

def train_model():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    import joblib
    import os

    if not os.path.exists(FEATURE_DATA):
        print("[-] Feature data not found. Run build_feature_dataset() first.")
        return

    df = pd.read_csv(FEATURE_DATA)
    
    # Drop non-feature columns if they exist (like 'url' if it was kept, though it wasn't in build_feature_dataset)
    # Based on build_feature_dataset, we have feature columns + 'label'
    
    X = df.drop(columns=["label"])
    y = df["label"]

    # Simple train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True, stratify=y)

    print(f"[+] Training model with {len(X_train)} samples...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"[+] Model Accuracy: {acc:.2f}")

    # Save
    model_path = "model/saved_models.pkl"
    joblib.dump(model, model_path)
    print(f"[+] Model saved to {model_path}")