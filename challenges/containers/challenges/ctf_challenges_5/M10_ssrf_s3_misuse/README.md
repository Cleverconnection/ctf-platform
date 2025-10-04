# Desafio M10 — SSRF Explorando Endpoint S3

## Descrição
Um proxy corporativo deveria permitir apenas URLs externas, mas aceita qualquer destino HTTP/HTTPS. Isso possibilita atingir um endpoint S3 interno que só autoriza acessos originados da própria máquina, expondo relatórios com a flag.

## Objetivos de Aprendizagem
- Construir SSRF para atingir serviços locais expostos pela aplicação.
- Entender como endpoints de armazenamento simulam ACLs baseadas em IP.
- Manipular parâmetros de consulta para ajustar cabeçalhos opcionais.

## Serviços Disponíveis
- `GET /api/proxy?url=` — Proxy inseguro utilizado pelo workflow.
- `GET /s3/internal/<key>` — Simulação de bucket S3 com controle por IP (somente localhost).
- `GET /` — Interface com instruções no tema Itaú.

## Como Executar
1. Suba o container.
2. Teste `/api/proxy?url=http://example.com` para entender o formato de resposta.
3. Troque a URL para um endereço local.

## Como Capturar a Flag
- Faça requisição a `/api/proxy?url=http://127.0.0.1:8080/s3/internal/statements/report.txt`.
- O proxy buscará o objeto localmente e retornará o conteúdo com a flag.
