from transformers import BertTokenizer, BertForSequenceClassification
import torch


tokenizer = BertTokenizer.from_pretrained("bert-large-uncased")
model = BertForSequenceClassification.from_pretrained("bert-large-uncased", torchscript=True)
model.eval()

inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
print(inputs)
traced_model = torch.jit.trace(model, [inputs["input_ids"], inputs["token_type_ids"], inputs["attention_mask"]])
torch.jit.save(traced_model, "bert.pt")
# outputs = model(**inputs)
# print(outputs)

# last_hidden_states = outputs.last_hidden_state

# print(last_hidden_states)

# loaded_model = torch.jit.load("bert.pt")
# loaded_model.eval()

# for i in range(2):
#   result = loaded_model(**inputs)
#   print(result)