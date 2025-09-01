import re
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import gc

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
        
        # Carregamento lazy do modelo - só carrega quando necessário
        self.model = None
        self.tokenizer = None
        self.model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../fine_tuned_model"))
    
    def _load_model(self):
        """Carrega o modelo apenas quando necessário"""
        if self.model is None or self.tokenizer is None:
            print("Carregando modelo...")
            # Carregar modelo com configurações de baixa memória
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                low_cpu_mem_usage=True
            )
            
            # Modo de avaliação para economizar memória
            self.model.eval()
            
            # Forçar garbage collection
            gc.collect()
            print("Modelo carregado com sucesso!")

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
            # Carregar modelo apenas quando necessário
            self._load_model()
            
            # Usar tokenizer e modelo diretamente para economizar memória
            inputs = self.tokenizer(
                processed_text, 
                return_tensors="pt", 
                truncation=True, 
                padding=True, 
                max_length=256
            )
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                predicted_class = torch.argmax(predictions, dim=-1).item()
                confidence = predictions[0][predicted_class].item()
            
            # Limpar tensores da memória
            del inputs, outputs, predictions
            gc.collect()
            
            label_map = {0: "Produtivo", 1: "Improdutivo"}
            category = label_map[predicted_class]
            score = confidence * 100
            
            return category, score
        except Exception as e:
            print("Erro na classificação:", e)
            raise

    def generate_response(self, category):
        if category == "Produtivo":
            return "Recebemos sua solicitação e em breve entraremos em contato. Obrigado!"
        else:
            return "Obrigado pelo carinho! Tenha um ótimo dia!"