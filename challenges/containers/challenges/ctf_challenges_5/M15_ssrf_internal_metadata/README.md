# Desafio M15 — SSRF contra Metadata Service

## Descrição
Um recurso de geração de relatórios aceita URLs arbitrárias e as requisita do lado do servidor. Isso possibilita atingir o endpoint de metadata da infraestrutura, restrito a chamadas locais, que expõe credenciais com a flag.

## Objetivos de Aprendizagem
- Investigar SSRF para atingir serviços de metadata.
- Analisar respostas JSON retornadas pelo serviço interno.
- Entender a criticidade de proteger credenciais temporárias de instâncias.

## Serviços Disponíveis
- `GET /api/report?url=` — Fetch remoto sem validação de destino.
- `GET /metadata/iam` — Metadata service simulado com credenciais (somente localhost).

## Como Executar
1. Suba o container.
2. Teste `/api/report?url=http://example.com` para ver a resposta padrão.
3. Aponte para o metadata service.

## Como Capturar a Flag
- Envie `GET /api/report?url=http://127.0.0.1:8080/metadata/iam`.
- A resposta conterá o JSON com `SecretAccessKey` igual à flag.
