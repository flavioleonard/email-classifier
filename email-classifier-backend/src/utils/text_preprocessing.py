from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenization
    words = text.split()
    
    # Remove stop words
    words = remove_stop_words(words)
    
    # Apply stemming
    words = apply_stemming(words)
    
    # Apply lemmatization
    words = apply_lemmatization(words)
    
    return ' '.join(words)

def remove_stop_words(words):
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word not in stop_words]

def apply_stemming(words):
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in words]

def apply_lemmatization(words):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]