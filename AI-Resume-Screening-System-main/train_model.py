import pandas as pd
import joblib

from preprocess import clean_resume

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load Dataset
df = pd.read_csv("dataset/resumes.csv")

# Clean Resume
df["Resume"] = df["Resume"].apply(clean_resume)

# Encode Category
encoder = LabelEncoder()
df["Category"] = encoder.fit_transform(df["Category"])

# TF-IDF
tfidf = TfidfVectorizer(stop_words="english", max_features=5000)

X = tfidf.fit_transform(df["Resume"])
y = df["Category"]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Model
model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

prediction = model.predict(X_test)

accuracy = accuracy_score(y_test, prediction)

print("Accuracy :", accuracy)

# Save Files
joblib.dump(model, "model/model.pkl")
joblib.dump(tfidf, "model/tfidf.pkl")
joblib.dump(encoder, "model/label_encoder.pkl")

print("Model Saved Successfully")