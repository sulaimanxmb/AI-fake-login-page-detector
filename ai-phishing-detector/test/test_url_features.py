import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from features.url_features import extract_url_features

test_urls = [
    "https://example.com/login",
    "http://secure-login-paypal.tk/account",
    "http://192.168.1.10/login",
    "https://accounts.google.com"
]

for url in test_urls:
    print(url)
    print(extract_url_features(url))
    print("-" * 40)