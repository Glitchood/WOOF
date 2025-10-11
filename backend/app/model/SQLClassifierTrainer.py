import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import (
    classification_report,
    precision_recall_fscore_support,
    roc_auc_score,
    roc_curve,
)
import pickle

# SQL injection strings - https://huggingface.co/datasets/firdhokk/autotrain-data-sql-injection
df = pd.read_csv("backend/app/model/raw_SQL_I.csv")
df = df.rename(columns={"Data": "text"})


def clean_text(s):
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


df["text"] = df["text"].astype(str).map(clean_text)
print(df.head())
X = df["text"].values
y = df["Label"].values
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

filename = "app/model/trained_model.pkl"

tfidf = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 6), max_features=30000)
clf = LogisticRegression(max_iter=1000, class_weight="balanced")
pipe = Pipeline([("tfidf", tfidf), ("clf", clf)])
pipe.fit(X_train, y_train)

with open(filename, "wb") as file:
    pickle.dump(pipe, file)

y_pred = pipe.predict(X_test)
print(classification_report(y_test, y_pred))
print("ROC AUC:", roc_auc_score(y_test, pipe.predict_proba(X_test)[:, 1]))
