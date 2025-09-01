# Email Classifier - Sistema de Classificação de Produtividade de Emails

Um sistema inteligente que classifica emails como "Produtivo" ou "Improdutivo" usando modelos de machine learning baseados em transformers, com uma API REST desenvolvida em FastAPI.

## 🚀 Funcionalidades

- **Classificação automática** de emails em categorias de produtividade
- **Suporte múltiplos formatos**: texto direto, arquivos .txt e .pdf
- **API REST** para integração com outras aplicações
- **Modelo personalizado** fine-tuned com DistilBERT multilingual
- **Pré-processamento avançado** de texto com NLTK
- **Respostas sugeridas** baseadas na classificação
- **Métricas de avaliação** do modelo

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python, FastAPI
- **Machine Learning**: Transformers (Hugging Face), PyTorch
- **Processamento de Texto**: NLTK, scikit-learn
- **Análise de Dados**: pandas, numpy
- **Leitura de Arquivos**: PyPDF2
- **Configuração**: YAML, python-dotenv

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. **Clone o repositório**

```bash
git clone <seu-repositorio>
cd email-classifier
```

2. **Crie um ambiente virtual**

```bash
python -m venv venv
```

3. **Ative o ambiente virtual**

No Windows (PowerShell):

```powershell
venv\Scripts\Activate.ps1
```

No Windows (Command Prompt):

```cmd
venv\Scripts\activate
```

No Linux/Mac:

```bash
source venv/bin/activate
```

4. **Instale as dependências**

```bash
cd email-classifier-backend
pip install -r requirements.txt
```

5. **Configure os recursos do NLTK** (primeira execução)

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

## 🚀 Como Executar

### Iniciar o servidor da API

```bash
python -m src.main
```

O servidor estará disponível em: `http://localhost:8000`

### Documentação da API

Acesse a documentação interativa em: `http://localhost:8000/docs`

## 📁 Estrutura do Projeto

```
email-classifier-backend/
├── src/
│   ├── api/
│   │   └── routes.py          # Rotas da API REST
│   ├── models/
│   │   └── classification.py  # Modelos Pydantic
│   ├── services/
│   │   ├── email_processor.py # Processamento de emails
│   │   └── nlp_service.py     # Serviços de NLP
│   ├── utils/
│   │   └── text_preprocessing.py # Utilitários de pré-processamento
│   ├── fine_tuned_model/      # Modelo treinado
│   ├── train.py               # Script de treinamento
│   ├── predict.py             # Script de predição
│   ├── evaluate.py            # Avaliação do modelo
│   └── main.py                # Ponto de entrada da aplicação
├── tests/                     # Testes unitários
├── requirements.txt           # Dependências Python
└── README.md
```

## 🔌 Uso da API

### Classificar Email via Texto

```bash
curl -X POST "http://localhost:8000/api/classify-email" \
  -H "Content-Type: multipart/form-data" \
  -F "text=Seu texto do email aqui"
```

### Classificar Email via Arquivo

```bash
curl -X POST "http://localhost:8000/api/classify-email" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@caminho/para/seu/arquivo.txt"
```

### Resposta da API

```json
{
  "category": "Produtivo",
  "confidence": 0.87,
  "suggested_response": "Este email requer atenção prioritária...",
  "processed_text": "texto processado..."
}
```

## 🧠 Modelo de Machine Learning

O sistema utiliza um modelo **DistilBERT multilingual** fine-tuned para classificação de produtividade de emails em português e inglês.

### Treinamento do Modelo

```bash
python -m src.train
```

### Avaliação do Modelo

```bash
python -m src.evaluate
```

### Predições Standalone

```bash
python -m src.predict
```

## 📊 Métricas de Performance

O modelo é avaliado usando:

- **Accuracy** (Acurácia)
- **Precision** (Precisão)
- **Recall** (Revocação)
- **F1-Score**

## 🔧 Configuração

Crie um arquivo `config.yaml` para personalizar configurações:

```yaml
model:
  name: "distilbert-base-multilingual-cased"
  path: "src/fine_tuned_model"
data:
  train_data_path: "data/emails_classificados.csv"
  test_data_path: "data/test_emails.csv"
```

## 🧪 Testes

Execute os testes unitários:

```bash
python -m pytest tests/
```

## 📝 Formato dos Dados de Treinamento

O arquivo CSV deve conter as colunas:

- `Email`: Texto do email
- `Classificacao`: "Produtivo" ou "Improdutivo"

Exemplo:

```csv
Email,Classificacao
"Reunião importante sobre projeto X","Produtivo"
"Spam promocional","Improdutivo"
```

## 🔄 Pipeline de Processamento

1. **Pré-processamento**: Limpeza e normalização do texto
2. **Tokenização**: Conversão para tokens do modelo
3. **Classificação**: Predição usando modelo fine-tuned
4. **Pós-processamento**: Geração de resposta sugerida

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Seu Nome** - _Desenvolvimento inicial_ - [Seu GitHub](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- Hugging Face pela biblioteca Transformers
- OpenAI pela inspiração em sistemas de classificação
- Comunidade Python pelo ecossistema de ferramentas
