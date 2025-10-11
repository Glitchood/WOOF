import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion
import pickle

filename = "app/model/trained_model.pkl"
with open(filename, "rb") as file:
    pipe = pickle.load(file)

def checkSQL(s):
    return pipe.predict(np.array([s])) == 1
