from transformers import BertTokenizer, BertForSequenceClassification

# Load tokenizer and PyTorch weights form the Hub
tokenizer = BertTokenizer.from_pretrained("bert-large-uncased")
pt_model = BertForSequenceClassification.from_pretrained("bert-large-uncased")

tokenizer.save_pretrained("bert-pt")
pt_model.save_pretrained("bert-pt")