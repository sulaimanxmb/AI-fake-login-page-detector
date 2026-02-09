from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_html_features(html: str, url: str) -> dict:
    features = {
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

    soup = BeautifulSoup(html, "html.parser")
    page_domain = urlparse(url).netloc

    # Password field
    if soup.find("input", {"type": "password"}):
        features["has_password_field"] = 1

    # Forms
    forms = soup.find_all("form")
    features["num_forms"] = len(forms)

    for form in forms:
        action = form.get("action")
        if action and action.startswith("http"):
            action_domain = urlparse(action).netloc
            # Check if domain is different and not just a subdomain/empty
            if page_domain and action_domain and page_domain not in action_domain:
                features["external_form_action"] = 1

    # Hidden inputs
    hidden_inputs = soup.find_all("input", {"type": "hidden"})
    features["hidden_inputs"] = len(hidden_inputs)

    # IFrames
    features["num_iframes"] = len(soup.find_all("iframe"))

    # --- NEW SOURCE CODE FEATURES ---

    # 1. Suspicious Keywords (Text Analysis)
    text_content = soup.get_text().lower()
    keywords = ["verify", "account", "update", "suspended", "bank", "security", "urgent", "confirm"]
    features["suspicious_keywords"] = sum(text_content.count(kw) for kw in keywords)

    # 2. Suspicious JavaScript (Source Analysis)
    scripts = soup.find_all("script")
    for script in scripts:
        if script.string:
            js_code = script.string.lower()
            if "eval(" in js_code or "unescape(" in js_code or "document.write(" in js_code:
                features["has_suspicious_js"] = 1
                break

    # 3. External Resources Ratio (Visual/Asset Analysis)
    # Check images and scripts to see if they are hosted elsewhere (common in cloning)
    resources = soup.find_all(["img", "script", "link"])
    total_resources = len(resources)
    external_resources = 0
    
    if total_resources > 0:
        for res in resources:
            src = res.get("src") or res.get("href")
            if src and src.startswith("http"):
                res_domain = urlparse(src).netloc
                if page_domain and res_domain and page_domain not in res_domain:
                    external_resources += 1
        features["external_resources_ratio"] = external_resources / total_resources

    # 4. Title Analysis
    if soup.title and soup.title.string:
        title = soup.title.string.lower()
        if "login" in title or "sign in" in title or "log in" in title:
            features["title_has_login"] = 1

    return features