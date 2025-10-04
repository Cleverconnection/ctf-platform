# Write-up — M16 Corrida em Verificação de Saldo

## Visão Geral do Vetor
O endpoint `/api/withdraw` realiza uma checagem de saldo, aguarda 0,6s e só então debita. Sem bloqueios, duas requisições simultâneas aprovam a retirada com base no mesmo saldo original, resultando em saldo negativo.

## Passo a Passo
1. Preparar script (Python `requests` + `ThreadPoolExecutor`).
2. Enviar duas chamadas simultâneas com `amount=1000`.
3. Observar que ambas retornam `status=ok`.
4. Consultar `/api/state` ou `/flag` para confirmar saldo negativo e capturar a flag.

## Evidências
- Logs mostrando duas respostas de saque aprovadas.
- Estado final com `checking: -500`.

## Mitigações Recomendadas
- Utilizar bloqueios, transações ou `compare-and-set` para garantir atomicidade.
- Implementar limites antifraude para impedir saldo negativo.
- Registrar e alertar sobre tentativas paralelas suspeitas.
