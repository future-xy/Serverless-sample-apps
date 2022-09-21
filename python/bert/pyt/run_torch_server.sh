python download.py
torchserve --stop
torch-model-archiver --model-name bert-pyt --version 1.0  --serialized-file bert.pt --handler bert_handler.py 
mv bert-pyt.mar model_store/
torchserve --start --ncs --model-store model_store --models bert=bert-pyt.mar

# curl -X POST http://127.0.0.1:8080/predictions/bert -T ./input.json
# ./build_image.sh -g -cv cu113 -t futurexy/torchserve:latest