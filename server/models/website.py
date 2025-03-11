import joblib
import pandas as pd
import os
import re
import tldextract
from sklearn.ensemble import RandomForestClassifier 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dataset_path = os.path.join(base_dir, "datasets", "dataset_website.csv")

df = pd.read_csv(dataset_path)

df["label"] = df["label"].apply(lambda x: "phishing" if x.lower() == "phishing" else "benign")

def extract_features(url):
    extracted = tldextract.extract(url)
    domain = extracted.domain
    subdomain = extracted.subdomain
    suffix = extracted.suffix

    features = {
        "length": len(url),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_slashes": url.count("/"),
        "num_subdomains": len(subdomain.split(".")) if subdomain else 0,
        "has_https": 1 if url.startswith("https") else 0,
        "has_at_symbol": 1 if "@" in url else 0,
        "has_ip_address": 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0,
        "has_suspicious_words": 1 if any(word in url.lower() for word in ["login", "secure", "bank", "verify", "free", "paypal"]) else 0,
    }
    
    return features

feature_list = df["url"].apply(lambda x: extract_features(x))
X = pd.DataFrame(feature_list.tolist())
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"Website Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

model_path = os.path.join(base_dir, "models", "website_model.pkl")
joblib.dump(model, model_path)
print(f"Model saved as {model_path}")

def analyze_url(url):
    model = joblib.load(model_path)
    features = extract_features(url)
    features_df = pd.DataFrame([features]) 
    return model.predict(features_df)[0]
