import pandas as pd
import re
from urllib.parse import urlparse
import tldextract
from collections import Counter
import math
import os
import numpy as np

# Get the absolute path to the assets directory
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'src', 'assets')

# Biến toàn cục cho multiprocessing
char_probabilities = pd.read_csv(os.path.join(assets_dir, 'char_probabilities.csv')).set_index('Character')['Probability'].to_dict()
# Đọc danh sách top 100k domain từ Tranco
top_100k_tranco_list = set(pd.read_csv(os.path.join(assets_dir, 'tranco_5897N.csv'), header=None).iloc[:, 1].tolist())


# Các pattern và cấu hình
special_chars = "`%^&*;@!?#=+$|"
special_chars_domain = ".-_"
hex_pattern = re.compile(r'[a-fA-F0-9]{10,}')
common_keywords = {
    "password", "login", "secure", "account", "index", "token", "signin", 
    "update", "verify", "auth", "security", "confirm", "submit", "payment", 
    "invoice", "billing", "transaction", "transfer", "refund", "wire"
}
redirect_keywords = {"redirect=", "url=", "next=", "dest=", "destination=", "forward=", "go=", "to="}
ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')


# ⭐ Hàm trích xuất đặc trưng
def extract_features(url):
    url = url.strip("'\"")
    parsed_url = urlparse(url if urlparse(url).scheme else "http://" + url)

    extracted = tldextract.extract(url)
    domain = parsed_url.hostname or ""
    length = len(url)
    is_domain_ip = re.fullmatch(ip_pattern, domain)
    char_counts = Counter(domain)
    total_chars = sum(char_counts.values())
    domain_char_prob = {char: count / total_chars for char, count in char_counts.items()}

    features = [
        length,  # 1. length
        sum(1 for c in url if c in special_chars),  # 2. tachar
        int(any(kw in url.lower() for kw in common_keywords)),  # 3. hasKeyWords
        round(sum(len(m) for m in re.findall(hex_pattern, url)) / length, 15),  # 4. tahex
        round(sum(c.isdigit() for c in url) / length, 15),  # 5. tadigit
        url.count('.'),  # 6. numDots
        sum(c.isupper() for c in url),  # 7. countUpcase
        round(sum(c in "aeiou" for c in url.lower()) / length, 15),  # 8. numvo
        round(sum(c.isalpha() and c.lower() not in "aeiou" for c in url) / length, 15),  # 9. numco
        int(any(len(s) > 30 for s in re.findall(r'\S+', url))),  # 10. maxsub30
        round(len(parsed_url.path) / length, 15) if parsed_url.path else 0,  # 11. rapath
        1 if urlparse(url).scheme == "http"  else 0,
        1 if urlparse(url).scheme == "https" else 0,
        1 if parsed_url.netloc.startswith("www.") else 0,
        0 if is_domain_ip else len(extracted.subdomain.split('.')) if extracted.subdomain else 0,  # 15. numsdm
        round(len(domain) / length, 15) if domain else 0,  # 16. radomain
        round(sum(c in "aeiou" for c in domain.lower()) / len(domain), 15) if domain else 0,  # 18. tanv
        round(sum(c.isalpha() and c.lower() not in "aeiou" for c in domain) / len(domain), 15) if domain else 0,  # 19. tanco
        round(sum(c.isdigit() for c in domain) / len(domain), 15) if domain else 0,  # 20. tandi
        round(sum(c in special_chars_domain for c in domain) / len(domain), 15) if domain else 0,  # 21. tansc
        len(domain),  # 23. domain_len
        round(-sum(p * math.log2(p) for p in domain_char_prob.values()), 15) if domain else 0,  # 24. ent_char
        round(sum(domain.count(c) * char_probabilities.get(c, 0) for c in domain) / len(domain), 15) if domain and char_probabilities else 0,  # 25. eod
        0 if is_domain_ip else int(extracted.registered_domain in top_100k_tranco_list),  # 26. rank
        0 if is_domain_ip else int(extracted.suffix in {"com", "net", "org", "edu", "gov"}),  # 27. tld
        0 if is_domain_ip else int(extracted.suffix in {'tk', 'ml', 'cf', 'ga', 'gq', 'xyz', 'top', 'cn', 'ru', 'work', 'club', 'site'}),  # 29. hasSuspiciousTld
    ]
    feature_names = [
    "length", "tachar", "hasKeyWords", "tahex", "tadigit", "numDots", "countUpcase",
    "numvo", "numco", "maxsub30", "rapath", 'http','https','www',  "numsdm",
    "radomain", "tanv", "tanco", "tandi", "tansc",  "domain_len",
    "ent_char", "eod", "rank", "tld", "hasSuspiciousTld"
    ]
    df = pd.DataFrame([features],columns=feature_names)
    return df

def extract_features_text(text):
    """Extract features from text for phishing detection"""
    # Get character probabilities from training data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'char_probabilities.csv')
    char_probs = pd.read_csv(data_path)
    
    # Initialize feature vector
    features = np.zeros(len(char_probs.columns) - 1)  # -1 for label column
    
    # Calculate character frequencies
    text = text.lower()
    total_chars = len(text)
    if total_chars == 0:
        return features
        
    for i, char in enumerate(char_probs.columns[:-1]):  # Exclude label column
        features[i] = text.count(char) / total_chars
        
    return features


