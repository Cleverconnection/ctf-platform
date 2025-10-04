# Desafio M19 — Quebra de Cabeçalho Authorization

## Descrição
O serviço espera um cabeçalho `Authorization: Token token=<valor>;role=<perfil>` e converte todas as partes em um dicionário minúsculo. Ao enviar o token válido e definir `role=admin`, o backend concede acesso completo.

## Objetivos de Aprendizagem
- Inspecionar formatos personalizados de header Authorization.
- Manipular múltiplos parâmetros em um único header.
- Validar respostas diferenciadas conforme o role recebido.

## Serviços Disponíveis
- `GET /` — Exibe o token padrão (`svc-ops-2025`).
- `GET /api/secure` — Processa o header customizado e retorna a flag quando `role=admin`.

## Como Executar
1. Suba o container.
2. Monte o header `Authorization: Token token=svc-ops-2025;role=admin`.
3. Faça a requisição via `curl` ou ferramenta de testes.

## Como Capturar a Flag
- `curl -H "Authorization: Token token=svc-ops-2025;role=admin" http://localhost:8080/api/secure`
- A resposta JSON incluirá a flag no campo `flag`.
