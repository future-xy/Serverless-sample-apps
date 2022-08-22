# Build sample app
FROM golang:1.18 as builder

WORKDIR /go/src/github.com/future-xy/serverless-sample-apps
COPY go.mod go.mod
COPY go.sum go.sum

RUN  go mod download

COPY cmd/   cmd/

RUN go build -a -o http_server ./cmd/http_server

FROM gcr.io/distroless/base-debian10
WORKDIR /
COPY --from=builder /go/src/github.com/future-xy/serverless-sample-apps/http_server /http_server
EXPOSE 8080
USER nonroot:nonroot
ENTRYPOINT ["/http_server"]

