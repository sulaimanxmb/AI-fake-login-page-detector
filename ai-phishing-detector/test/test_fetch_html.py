import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Correct import
from utils.fetch_html import fetch_html

test_urls = [
    "https://example.com",
    "https://github.com/login",
    "https://accounts.google.com",
    "http://nonexistent.example"
]

for url in test_urls:
    print("=" * 60)
    print("URL:", url)

    html = fetch_html(url)

    if html:
        print("HTML fetched: YES")
        print("HTML length:", len(html))
    else:
        print("HTML fetched: NO")