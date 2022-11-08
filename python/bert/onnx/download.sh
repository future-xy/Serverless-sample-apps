# This file downloads bert-large-uncased model in onnx format.
# python -m transformers.onnx --model=bert-large-uncased ckpt/
python download.py
python -m transformers.onnx --model=bert-pt --feature=sequence-classification bert-pt-onnx/