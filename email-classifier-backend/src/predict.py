from transformers import pipeline
import pandas as pd
import yaml

# Load configuration
with open("config.yaml", 'r') as file:
    config = yaml.safe_load(file)

# Load the fine-tuned model
model_name = config['model']['name']
classifier = pipeline("zero-shot-classification", model=model_name)

def predict_email_category(email_text):
    """Predict the category of the email and return the category and confidence score."""
    labels = ["Produtivo", "Improdutivo"]
    result = classifier(email_text, candidate_labels=labels)
    category = result['labels'][0]
    confidence = result['scores'][0]
    return category, confidence

if __name__ == "__main__":
    # Example usage
    email_data = pd.read_csv("data/emails_classificados.csv")
    for index, row in email_data.iterrows():
        email_text = row['Email']
        category, confidence = predict_email_category(email_text)
        print(f"Email: {email_text}\nPredicted Category: {category} (Confidence: {confidence:.2f})\n")