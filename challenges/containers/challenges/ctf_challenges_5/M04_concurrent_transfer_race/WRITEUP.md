# Write-up — M04 Corrida em Transferências Concorrentes

## Visão Geral do Vetor
O endpoint `/api/transfer` valida o saldo antes de aguardar 0,7s e só então aplica o débito. Em requisições paralelas, ambas calculam o saldo com base no mesmo valor inicial e executam o débito depois, permitindo sobreposição. A conta de destino recebe o crédito somado de todas as transferências.

## Passo a Passo
1. Capture o corpo JSON esperado: `{ "from": "pagamentos", "to": "fraude", "amount": 3000 }`.
2. Utilize um script (ex.: Python com `threading` ou `asyncio`) para enviar duas requisições POST simultâneas.
3. Consulte `/api/state` após a corrida para verificar que `pagamentos` ficou negativo ou com saldo incorreto e `fraude` cresceu mais do que o permitido.
4. Acesse `/flag` para coletar a flag.

## Evidências
- Respostas sucessivas de `/api/transfer` retornando `status=ok` mesmo com a conta origem sem saldo suficiente para a segunda transação.
- Estado final exibindo `fraude` ≥ 4000 no JSON.

## Mitigações Recomendadas
- Utilizar bloqueios transacionais ou operações atômicas no backend.
- Implementar controle otimista com verificação de versão do saldo (compare-and-swap).
- Registrar tentativas concorrentes para detecção de comportamento anômalo.
