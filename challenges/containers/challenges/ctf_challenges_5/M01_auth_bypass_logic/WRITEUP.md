# Write-up — M01 Auth Bypass Logic

## Visão Geral do Vetor
A API confia que o cliente seguirá o fluxo correto de autenticação. O endpoint `/api/complete` apenas verifica se o campo `step` recebido possui o valor `mfa_ok`, sem garantir que o servidor tenha marcado esse estado. Basta reaproveitar um `session_id` válido e forjar a etapa final.

## Passo a Passo
1. **Obter `session_id`** — Envie `POST /api/start` com as credenciais fornecidas na página (`analyst` / `senh@F0rte`). A resposta inclui `session_id` e indica o próximo passo.
2. **Ignorar MFA** — Pule `/api/mfa` e chame `POST /api/complete` com `{"session_id":"<valor>","step":"mfa_ok"}`.
3. **Receber Flag** — O servidor devolve `{ "status": "admin", "flag": "ITAU2025{...}" }`, evidenciando o bypass.

## Evidências
- Captura das respostas HTTP com status 200 e o corpo contendo o campo `flag`.
- Logs da aplicação registrando o `session_id` com `step=password_ok`, sem atualização para `mfa_ok`.

## Mitigações Recomendadas
- Manter estado do fluxo exclusivamente no servidor, ignorando o campo `step` fornecido pelo cliente.
- Introduzir tokens únicos por etapa e invalidar a sessão ao detectar saltos de fase.
- Registrar tentativas fora de ordem e acionar alertas antifraude.
