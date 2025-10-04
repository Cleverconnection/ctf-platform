# Write-up — M03 SSRF em Serviço Interno

## Visão Geral do Vetor
O endpoint `/api/fetch` aceita qualquer URL HTTP e apenas bloqueia explicitamente `localhost` e `127.0.0.1`. Endereços alternativos (`127.1`) passam pelo filtro e fazem com que o servidor execute uma requisição a partir da rede interna. Ao adicionar `internal_key` como parâmetro, o proxy reenvia o cabeçalho `X-Internal-Key`, satisfazendo a validação do endpoint restrito.

## Passo a Passo
1. Teste `/api/fetch?url=http://example.com` para observar o comportamento do proxy.
2. Troque o host por `http://127.1:8080/health` para confirmar que o backend alcança serviços locais.
3. Ajuste a URL para `http://127.1:8080/internal/ops` e forneça `internal_key=svc-admin-2025`.
4. Receba como resposta um JSON contendo a flag e a mensagem de aviso do endpoint.

## Evidências
- Logs HTTP mostrando a chamada SSRF com `remote_addr=127.0.0.1` no serviço interno.
- Resposta JSON contendo `{ "flag": "ITAU2025{...}" }` devolvida ao cliente.

## Mitigações Recomendadas
- Normalizar e validar endereços IP resolvidos (incluindo notações alternativas) antes de efetuar requisições.
- Manter listas de permissão explícitas (allowlist) para destinos confiáveis.
- Remover a opção de repassar cabeçalhos sensíveis informados pelo cliente.
