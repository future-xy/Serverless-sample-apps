IMG ?= http_server_sample:latest

http_server: fmt vet
	go build -o bin/http_server ./cmd/http_server/main.go

docker-build: fmt vet
	docker build . -t ${KO_DOCKER_REPO}/${IMG}

docker-push:
	docker push ${KO_DOCKER_REPO}/${IMG}

fmt:
	go fmt ./cmd/...

vet:
	go vet ./cmd/...
