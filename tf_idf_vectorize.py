import numpy as np
import pandas as pd
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

class Vectorizer:
    def __init__(self, k=10000):
        self.vectorizer = TfidfVectorizer()
        self.vocab = None
        self.k = k

    def fit(self, texts):
        self.k = min(self.k, len(set(" ".join(texts).split())))

        self.vectorizer.fit(texts)
        counts = Counter(' '.join(texts).split())
        self.vocab = [key for key, val in counts.most_common(self.k)]

    def transform(self, texts):
        return self.vectorizer.transform(texts)

    def fit_transform(self, texts):
        self.fit(texts)
        return self.transform(texts)

    def get_tf_idf(self, texts):
        vectorized = self.transform(texts)
        names = self.vectorizer.get_feature_names_out()

        return self.tfidf_in_vocab(vectorized, names)

    def tfidf_in_vocab(self, vectorized, names):
        df = pd.DataFrame(vectorized.todense(), columns=names)
        sent_matr = df.drop(list(df.columns.difference(self.vocab)), axis=1)
        res_matr = np.zeros((sent_matr.shape[0], len(self.vocab)))
        for i, token in enumerate(self.vocab):
            if token in sent_matr.columns:
                res_matr[:, i] = sent_matr[token].to_numpy()
        return res_matr
