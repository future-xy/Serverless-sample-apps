# Serverless-sample-apps
Applications for serverless test

### Quick Start
Deploy http server
```bash
make docker-build
kubectl apply -f install/http_server.yaml
```
Test http server
1. Get pod name
```bash
kubectl get pods
```
2. Forward port in another terminal
```bash
kubectl port-forward <pod name> 8080:8080
```

3. Test
```bash
curl localhost:8080
```

## Model Test
This part shows how to download models from [Hugging Face](https://huggingface.co/models) (via [Transformers](https://github.com/huggingface/transformers)).

### Prerequests
1. Create a virtual environment.
2. Install [PyTorch](https://pytorch.org/get-started/locally/) and [Transformers](https://huggingface.co/docs/transformers/installation)

### Download the model
Please note, by default, the following line will download 'opt-125m' which contains 125 million parameters and try to distribute the model over all available devices.
```bash
python python/opt/download.py
```

To limit the devices used, please set CUDA_VISIBLE_DEVICES. For example, the following lines run two `opt-13b` models on GPU 0,1 and 2,3, which is the case shown in the below figure.
```bash
CUDA_VISIBLE_DEVICES=0,1 python python/opt/download.py --model-name opt-13b &
CUDA_VISIBLE_DEVICES=2,3 python python/opt/download.py --model-name opt-13b &
```
<img width="322" alt="image" src="https://user-images.githubusercontent.com/31511840/216121121-17b480d9-9bf2-4667-aac5-985b08002668.png">
