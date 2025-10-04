# Write-up — M05 Reprocessamento de Pagamentos

## Visão Geral do Vetor
A rota `/api/pay` aceita qualquer `reference` e não verifica se a transação já foi processada. Como efeito colateral, o programa de fidelidade soma o valor recebido ao saldo a cada POST, mesmo que seja a mesma fatura.

## Passo a Passo
1. Enviar `POST /api/pay` com `{"reference":"fatura-001","amount":1000}`.
2. Repetir a chamada múltiplas vezes usando `curl` em loop ou `while true; do ...; done`.
3. Consultar `/api/ledger` para observar entradas duplicadas com o mesmo `reference`.
4. Quando o campo `loyalty` atingir 5000, solicitar `/flag`.

## Evidências
- Respostas consecutivas com `status=ok` e contagem crescente (`"count"`).
- Histórico mostrando diversas entradas idênticas para a mesma referência.

## Mitigações Recomendadas
- Exigir chaves de idempotência (`Idempotency-Key`) e rejeitar replays.
- Registrar transações com hash único e abortar se já existirem.
- Implementar auditoria de fraude para detectar padrões repetitivos.
