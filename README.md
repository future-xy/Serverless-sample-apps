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