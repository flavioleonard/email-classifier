import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch

def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df['Email'].tolist(), df['Classificacao'].tolist()

def preprocess_data(emails, labels):
    tokenizer = AutoTokenizer.from_pretrained("MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
    encodings = tokenizer(emails, truncation=True, padding=True, max_length=512)
    label_map = {"Produtivo": 0, "Improdutivo": 1}
    labels = [label_map[label] for label in labels]
    return encodings, labels, tokenizer

class EmailDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def fine_tune_model(encodings, labels, tokenizer):
    model = AutoModelForSequenceClassification.from_pretrained(
        "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli", 
        num_labels=2,
        ignore_mismatched_sizes=True
    )
    train_indices, val_indices = train_test_split(range(len(labels)), test_size=0.2, random_state=42)
    train_encodings = {k: [v[i] for i in train_indices] for k, v in encodings.items()}
    val_encodings = {k: [v[i] for i in val_indices] for k, v in encodings.items()}
    train_labels = [labels[i] for i in train_indices]
    val_labels = [labels[i] for i in val_indices]
    train_dataset = EmailDataset(train_encodings, train_labels)
    val_dataset = EmailDataset(val_encodings, val_labels)
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )
    trainer.train()
    model.save_pretrained('./fine_tuned_model')
    tokenizer.save_pretrained('./fine_tuned_model')

if __name__ == "__main__":
    emails, labels = load_dataset('emails_classificados.csv')
    encodings, labels, tokenizer = preprocess_data(emails, labels)
    fine_tune_model(encodings, labels, tokenizer)