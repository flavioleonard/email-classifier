import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from transformers import pipeline
import yaml

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def evaluate_model(model_path, test_data_path):
    # Load the fine-tuned model
    classifier = pipeline("zero-shot-classification", model=model_path)

    # Load the test data
    test_data = pd.read_csv(test_data_path)
    emails = test_data['Email'].tolist()
    true_labels = test_data['Classificacao'].tolist()

    # Make predictions
    predictions = classifier(emails, candidate_labels=["Produtivo", "Improdutivo"])
    
    # Extract predicted labels
    predicted_labels = [result['labels'][0] for result in predictions]

    # Calculate metrics
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels, pos_label="Produtivo", average='binary')
    recall = recall_score(true_labels, predicted_labels, pos_label="Produtivo", average='binary')
    f1 = f1_score(true_labels, predicted_labels, pos_label="Produtivo", average='binary')

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }

if __name__ == "__main__":
    config = load_config("config.yaml")
    model_path = config['model']['path']
    test_data_path = config['data']['test_data_path']
    
    metrics = evaluate_model(model_path, test_data_path)
    print("Evaluation Metrics:")
    print(metrics)