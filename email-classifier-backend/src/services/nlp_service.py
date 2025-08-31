import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
from transformers import pipeline
import torch
import os


class NLPService:
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
        self.stop_words = set(stopwords.words('portuguese'))
        self.stop_words.update(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../fine_tuned_model"))

        self.classifier = pipeline(
            "text-classification",
            model=model_path,
            tokenizer=model_path,
            device=0 if torch.cuda.is_available() else -1
        )
        self.labels = ["Produtivo", "Improdutivo"]
        

    def preprocess_text(self, text):
        """Aplica pré-processamento no texto"""
        text = text.lower()
        text = re.sub(r'\S+@\S+', '', text) 
        text = re.sub(r'http\S+|www\S+', '', text)  
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\d+', '', text)  
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in self.stop_words]
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        tokens = [token for token in tokens if len(token) > 2]
        return ' '.join(tokens)
    
    def classify_email_productivity(self, processed_text):
        """Classifica email como Produtivo ou Improdutivo usando modelo fine-tunado"""
        try:
            result = self.classifier(processed_text)
            label_map = {"LABEL_0": "Produtivo", "LABEL_1": "Improdutivo"}
            category = label_map.get(result[0]['label'], result[0]['label'])
            score = result[0]['score'] * 100
            return category, score
        except Exception as e:
            import traceback
            print("Erro na classificação:", e)
            traceback.print_exc()
            raise

    def generate_response(self, category):
        """Gera resposta automática baseada na categoria"""
        if category == "Produtivo":
            return "Recebemos sua solicitação e em breve entraremos em contato. Obrigado!"
        else:
            return "Obrigado pelo carinho! Tenha um ótimo dia!"