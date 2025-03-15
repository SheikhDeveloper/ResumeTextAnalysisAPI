import sklearn
import pickle
from tf_idf_vectorize import Vectorizer
from nltk.tokenize import WordPunctTokenizer

class ModelManager:
    def __init__(self):
        with open('vectorizer.pickle', 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open('model.pickle', 'rb') as f:
            self.model = pickle.load(f)
        self.preprocess = lambda text: ' '.join(WordPunctTokenizer().tokenize(text.lower()))

    def get_prediction(text: str) -> str:
        '''
        @brief: Analyzes the resume's content and predicts whether it is substantive or not
        @param text: str - Text of the resume to analyze
        @return: bool - True if the resume is substantive, False otherwise
        '''
        text = self.preprocess(text)
        text = self.vectorizer.get_tf_idf(text)
        return self.model.predict([text])
