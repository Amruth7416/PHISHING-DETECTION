import joblib
import pandas as pd
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dataset_path = os.path.join(base_dir, "datasets", "dataset_email.csv")
df = pd.read_csv(dataset_path)

df.columns = df.columns.astype(str)

df["label"] = df["label"].apply(lambda x: "suspicious" if x.lower() in ["malicious", "phishing"] else "benign")

def extract_email_features(text):
    features = {
        "num_words": len(text.split()),  
        "num_exclamation": text.count("!"),
        "num_dollar_signs": text.count("$"),
        "num_links": len(re.findall(r"https?://\S+", text)),
       "num_suspicious_words": sum(1 for word in [
    "urgent", "important", "immediate", "act now", "final notice", "limited time", "expiring soon",
    "verify", "security alert", "account compromised", "attention", "congratulations", "you won",
    "claim your prize", "lottery", "free gift", "exclusive offer", "money transfer", "wire transfer",
    "bitcoin", "investment opportunity", "cashback", "login", "password", "reset", "update account",
    "secure your account", "confirm your identity", "authentication required", "suspicious activity",
    "verify your email", "CEO request", "HR department", "payroll", "invoice", "payment due",
    "refund", "legal notice", "FBI", "IRS", "bank alert", "click here", "open attachment",
    "download now", "verify now", "your account will be locked", "respond immediately",
    "firewall update", "account suspension", "encryption required", "software update",
    "security breach"
] if word in text.lower()),

        "num_caps": sum(1 for char in text if char.isupper()) / max(len(text), 1), 
    }
    return features

vectorizer = TfidfVectorizer(max_features=3000)
X_text = vectorizer.fit_transform(df["email"])

feature_list = df["email"].apply(lambda x: extract_email_features(x))
X_additional = pd.DataFrame(feature_list.tolist())

X_text_df = pd.DataFrame(X_text.toarray(), index=df.index)

X_text_df = pd.DataFrame(X_text.toarray(), columns=[f"tfidf_{i}" for i in range(X_text.shape[1])])

X_additional = pd.DataFrame(X_additional)

X = pd.concat([X_text_df, X_additional], axis=1)
y = df["label"]

X.columns = X.columns.astype(str) 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"Email Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

model_path = os.path.join(base_dir, "models", "email_model.pkl")
joblib.dump((model, vectorizer), model_path)
print(f"Model saved as {model_path}")

def detect_email(email_text):
    if " " not in email_text and email_text.startswith(("http", "www")):
        return "Invalid input: Detected a URL instead of an email."

    model, vectorizer = joblib.load(model_path)

    features = extract_email_features(email_text)
    features_df = pd.DataFrame([features])

    text_features = vectorizer.transform([email_text]).toarray()
    text_features_df = pd.DataFrame(text_features)

    text_features_df.columns = text_features_df.columns.astype(str)
    features_df.columns = features_df.columns.astype(str)

    full_features = pd.concat([text_features_df, features_df], axis=1)

    expected_features = model.feature_names_in_
    full_features = full_features.reindex(columns=expected_features, fill_value=0)

    return model.predict(full_features)[0]
