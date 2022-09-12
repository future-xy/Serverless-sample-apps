import tensorflow as tf
from transformers import BertTokenizer
import requests
import json

sentence = "PhD students are not good at doing [MASK]."

# Load the corresponding tokenizer of our SavedModel
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased')

# Tokenize the sentence
inputs = tokenizer(sentence)

r = requests.post("http://localhost:8501/v1/models/bert_large_model:predict", data=json.dumps({"instances": [dict(inputs)]}))

result = json.loads(r.text)["predictions"][0]

# convert input_ids to tf tensor
input_ids = tf.convert_to_tensor(inputs.input_ids, dtype=tf.int32)
mask_token_index = tf.where((input_ids == tokenizer.mask_token_id))
selected_logits = tf.gather_nd(result, indices=mask_token_index)

predicted_token_id = tf.math.argmax(selected_logits, axis=-1)
print(tokenizer.decode(predicted_token_id))