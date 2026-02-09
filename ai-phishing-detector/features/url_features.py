import re
import tldextract
from urllib.parse import urlparse

def extract_url_features(url: str) -> dict:
    features = {}

    parsed = urlparse(url)
    domain = parsed.netloc

    features["url_length"] = len(url)
    features["num_dots"] = url.count(".")
    features["has_https"] = 1 if parsed.scheme == "https" else 0
    features["has_at"] = 1 if "@" in url else 0
    features["has_hyphen"] = 1 if "-" in domain else 0

    # IP address check
    ip_pattern = r"\b\d{1,3}(\.\d{1,3}){3}\b"
    features["has_ip"] = 1 if re.search(ip_pattern, domain) else 0

    # Subdomain count
    ext = tldextract.extract(url)
    features["num_subdomains"] = len(ext.subdomain.split(".")) if ext.subdomain else 0

    return features