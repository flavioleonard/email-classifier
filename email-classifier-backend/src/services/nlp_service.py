import re
import nltk


class NLPService:
    def __init__(self):
        from nltk.corpus import stopwords
        from nltk.stem import PorterStemmer, WordNetLemmatizer
        import nltk

        nltk.download('stopwords')
        nltk.download('wordnet')

        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_text(self, text):
        # Tokenize the text
        words = text.split()

        # Remove stop words and apply stemming/lemmatization
        processed_words = [
            self.lemmatizer.lemmatize(self.stemmer.stem(word.lower()))
            for word in words if word.lower() not in self.stop_words
        ]

        return ' '.join(processed_words)