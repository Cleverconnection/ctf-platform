# Write-up — M15 SSRF contra Metadata Service

## Visão Geral do Vetor
O endpoint `/api/report` aceita qualquer URL com esquema HTTP/HTTPS e não filtra IPs internos. O metadata service verifica apenas `remote_addr`, assumindo que clientes são locais. Como a requisição parte do próprio servidor, a checagem é satisfeita.

## Passo a Passo
1. Requisitar `/api/report?url=http://127.0.0.1:8080/metadata/iam`.
2. Receber resposta `{"status":200,"body":"{...}"}`.
3. Extrair `SecretAccessKey` (flag) do corpo JSON retornado.

## Evidências
- Resposta do report contendo o JSON com credenciais internas.
- Logs do metadata service registrando acesso local.

## Mitigações Recomendadas
- Bloquear faixas de IP internas (loopback, RFC1918, metadata) em funcionalidades SSRF.
- Implementar allowlist de destinos confiáveis.
- Requerer autenticação adicional ou proxies isolados para acessar metadata.
