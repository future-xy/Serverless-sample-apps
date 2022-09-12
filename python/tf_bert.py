import tensorflow as tf
from transformers import BertTokenizer, TFBertLMHeadModel

# download bert large uncased model
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased')
model = TFBertLMHeadModel.from_pretrained('bert-large-uncased')

inputs = tokenizer("The capital of France is [MASK].", return_tensors="tf")
logits = model(**inputs).logits

# retrieve index of [MASK]
mask_token_index = tf.where((inputs.input_ids == tokenizer.mask_token_id)[0])
print(logits.shape)
selected_logits = tf.gather_nd(logits[0], indices=mask_token_index)

predicted_token_id = tf.math.argmax(selected_logits, axis=-1)
print(predicted_token_id)
result=tokenizer.decode(predicted_token_id)
print(tokenizer.decode(predicted_token_id))

model.save_pretrained("bert_large", saved_model=True)

