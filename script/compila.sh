# WEB-101
docker compose exec chall-manager bash -lc '
  set -e
  cd /scenarios/web-101
  rm -rf .venv __pycache__ .pytest_cache *.pyc .cache
  [ -f go.mod ] || go mod init web-101
  go get github.com/pulumi/pulumi/sdk/v3@latest
  go get github.com/pulumi/pulumi-command/sdk/go/command/local@latest
  go get github.com/ctfer-io/chall-manager/sdk@latest
  go mod tidy
  CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -trimpath -ldflags="-s -w" -o main .
  chall-manager-cli scenario \
    --url http://localhost:8080 \
    --scenario registry:5000/web-101:2 \
    --directory . \
    --insecure
'

# WEB-102
docker compose exec chall-manager bash -lc '
  set -e
  cd /scenarios/web-102
  rm -rf .venv __pycache__ .pytest_cache *.pyc .cache
  [ -f go.mod ] || go mod init web-102
  go get github.com/pulumi/pulumi/sdk/v3@latest
  go get github.com/pulumi/pulumi-command/sdk/go/command/local@latest
  go get github.com/ctfer-io/chall-manager/sdk@latest
  go mod tidy
  CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -trimpath -ldflags="-s -w" -o main .
  chall-manager-cli scenario \
    --url http://localhost:8080 \
    --scenario registry:5000/web-102:latest \
    --directory . \
    --insecure
'
