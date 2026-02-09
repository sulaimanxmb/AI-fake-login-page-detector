import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from detect import extract_all_features

test_urls = [
    "https://example.com",
    "https://github.com/login",
    "http://192.168.1.10/login"
]

for url in test_urls:
    print("=" * 60)
    print("URL:", url)

    features = extract_all_features(url)

    for key, value in features.items():
        print(f"{key}: {value}")