import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import string
from transformers import pipeline
import torch

class NLPService:
    def __init__(self):
        # Download NLTK data if not already present
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
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        
        # Initialize classification pipeline
        self.classifier = pipeline(
            "text-classification",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=0 if torch.cuda.is_available() else -1
        )

    def preprocess_text(self, text):
        """Aplica técnicas de NLP para pré-processar o texto"""
        # Converter para minúsculas
        text = text.lower()
        
        # Remover emails e URLs
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remover pontuação
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remover números
        text = re.sub(r'\d+', '', text)
        
        # Tokenização
        tokens = word_tokenize(text)
        
        # Remoção de stop words
        tokens = [token for token in tokens if token not in self.stop_words]
        
        # Lemmatização
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        # Remover tokens muito curtos
        tokens = [token for token in tokens if len(token) > 2]
        
        return ' '.join(tokens)

    def classify_email_productivity(self, processed_text):
        """Classifica email como Produtivo ou Improdutivo"""
        
        # Palavras-chave para emails produtivos
        productive_keywords = [
            'suporte', 'problema', 'erro', 'bug', 'urgente', 'solicitacao',
            'duvida', 'questao', 'ajuda', 'assistencia', 'ticket', 'caso',
            'sistema', 'falha', 'correcao', 'atualizacao', 'status',
            'pendente', 'prazo', 'deadline', 'reuniao', 'projeto'
        ]
        
        # Palavras-chave para emails improdutivos
        unproductive_keywords = [
            'parabens', 'felicitacoes', 'obrigado', 'agradeco', 'sucesso',
            'aniversario', 'festa', 'social', 'pessoal', 'informal',
            'bom dia', 'boa tarde', 'cumprimento', 'saudacao'
        ]
        
        # Contar ocorrências de palavras-chave
        productive_count = sum(1 for keyword in productive_keywords if keyword in processed_text)
        unproductive_count = sum(1 for keyword in unproductive_keywords if keyword in processed_text)
        
        # Usar análise de sentimento como fator adicional
        sentiment_result = self.classifier(processed_text[:512])  # Limitar caracteres
        sentiment_score = sentiment_result[0]['score']
        
        # Lógica de classificação
        if productive_count > unproductive_count:
            confidence = (productive_count / (productive_count + unproductive_count + 1)) * 100
            return "Produtivo", confidence
        elif unproductive_count > productive_count:
            confidence = (unproductive_count / (productive_count + unproductive_count + 1)) * 100
            return "Improdutivo", confidence
        else:
            # Em caso de empate, usar sentimento
            if sentiment_result[0]['label'] in ['LABEL_0', 'negative']:
                return "Produtivo", sentiment_score * 100
            else:
                return "Improdutivo", sentiment_score * 100

    def generate_response(self, category, original_text):
        """Gera resposta automática baseada na categoria"""
        
        if category == "Produtivo":
            responses = [
                "Obrigado pelo seu contato. Recebemos sua solicitação e nossa equipe irá analisá-la. Retornaremos em breve com uma resposta.",
                "Sua solicitação foi registrada com sucesso. Nossa equipe técnica está analisando o caso e entrará em contato em até 24 horas.",
                "Agradecemos por entrar em contato. Sua questão é importante para nós e será tratada com prioridade.",
            ]
        else:
            responses = [
                "Muito obrigado pela sua mensagem! Ficamos felizes em receber seu contato.",
                "Agradecemos imensamente pelo seu feedback positivo. É muito importante para nossa equipe!",
                "Obrigado pela mensagem carinhosa. Ficamos gratos pelo reconhecimento!",
            ]
        
        # Retornar uma resposta aleatória baseada no hash do texto
        import hashlib
        hash_value = int(hashlib.md5(original_text.encode()).hexdigest(), 16)
        return responses[hash_value % len(responses)]