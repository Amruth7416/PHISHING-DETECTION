import joblib
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression 
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dataset_path = os.path.join(base_dir, "datasets", "dataset_phrases.csv")

df = pd.read_csv(dataset_path)

df["label"] = df["label"].apply(lambda x: "malicious" if x.lower() == "malicious" else "benign")

X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)

model = make_pipeline(TfidfVectorizer(), LogisticRegression()) 
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"Phrases Model Accuracy: {accuracy_score(y_test, y_pred):.2f}")

model_path = os.path.join(base_dir, "models", "phrases_model.pkl")
joblib.dump(model, model_path)
print(f"Model saved as {model_path}")

def predict_phrase(text):
    model = joblib.load(model_path)
    return model.predict([text])[0]
