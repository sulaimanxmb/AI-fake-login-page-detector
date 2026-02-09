import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.fetch_html import fetch_html
from features.html_features import extract_html_features

test_urls = [
    "https://github.com/login",
    "https://accounts.google.com",
    "https://example.com"
]

for url in test_urls:
    print("=" * 60)
    print("URL:", url)

    html = fetch_html(url)

    if html:
        features = extract_html_features(html, url)
        for key, value in features.items():
            print(f"{key}: {value}")
    else:
        print("HTML not fetched — skipping HTML feature extraction")