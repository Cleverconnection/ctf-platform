# Write-up — M17 Ataque por Timing em Autenticação

## Visão Geral do Vetor
A função `compare_slow` itera pelos caracteres e adiciona `time.sleep(DELAY)` quando os caracteres coincidem. Assim, uma tentativa com prefixo correto demora mais tempo que uma incorreta, expondo a senha por medição.

## Passo a Passo
1. Fixe `username=executivo` e tente senhas do tipo `0`, `1`, ..., medindo o tempo até o retorno. A maior latência indica o dígito correto para a primeira posição.
2. Repita para as posições seguintes, mantendo o prefixo correto conhecido.
3. Após descobrir `9246`, envie `POST /api/login` com a senha completa.
4. Receba a flag.

## Evidências
- Gráfico ou tabela dos tempos coletados demonstrando diferenças de ~120ms por caractere correto.
- Requisição final retornando `{ "status": "ok", "flag": "ITAU2025{...}" }`.

## Mitigações Recomendadas
- Usar comparação em tempo constante (`hmac.compare_digest`).
- Adicionar rate limiting e delays uniformes para tentativas falhas.
- Implementar mecanismos de lockout após múltiplas tentativas incorretas.
