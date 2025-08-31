from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import re
import string

def load_data(file_path):
    """Load the email dataset from a CSV file."""
    data = pd.read_csv(file_path)
    return data['Email'].tolist(), data['Classificacao'].tolist()

def preprocess_text(text):
    """Preprocess the input text by tokenizing, removing stop words, and lemmatizing."""
    text = text.lower()
    text = re.sub(r'\S+@\S+', '', text) 
    text = re.sub(r'http\S+|www\S+', '', text)  
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\d+', '', text)  
    tokens = word_tokenize(text)
    
    stop_words = set(stopwords.words('portuguese')).union(set(stopwords.words('english')))
    lemmatizer = WordNetLemmatizer()
    
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = [token for token in tokens if len(token) > 2]
    
    return ' '.join(tokens)