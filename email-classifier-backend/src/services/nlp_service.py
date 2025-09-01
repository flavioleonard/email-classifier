import re
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
from transformers import pipeline
import torch

class NLPService:
    def __init__(self):
        # Configurar diretório NLTK para produção
        if 'RENDER' in os.environ:
            nltk_data_path = os.path.join(os.path.dirname(__file__), '../../nltk_data')
            nltk.data.path.append(nltk_data_path)
        
        # Garantir recursos do NLTK
        for resource in ['punkt', 'stopwords', 'wordnet']:
            try:
                if resource == 'punkt':
                    nltk.data.find('tokenizers/punkt')
                else:
                    nltk.data.find(f'corpora/{resource}')
            except LookupError:
                try:
                    nltk.download(resource, quiet=True)
                except:
                    print(f"Falha ao baixar {resource}")
        
        self.stop_words = set(stopwords.words('portuguese')) | set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../fine_tuned_model"))
        self.classifier = pipeline(
            "text-classification",
            model=model_path,
            tokenizer=model_path,
            device=0 if torch.cuda.is_available() else -1
        )

    # ...existing code...
    def preprocess_text(self, text):
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
        try:
            result = self.classifier(processed_text)
            label_map = {"LABEL_0": "Produtivo", "LABEL_1": "Improdutivo"}
            category = label_map.get(result[0]['label'], result[0]['label'])
            score = result[0]['score'] * 100
            return category, score
        except Exception as e:
            print("Erro na classificação:", e)
            raise

    def generate_response(self, category):
        if category == "Produtivo":
            return "Recebemos sua solicitação e em breve entraremos em contato. Obrigado!"
        else:
            return "Obrigado pelo carinho! Tenha um ótimo dia!"