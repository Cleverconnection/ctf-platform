# Desafio M16 — Corrida em Verificação de Saldo

## Descrição
O endpoint de saque consulta o saldo e, antes de subtrair o valor, espera 0,6s. Enquanto isso, outras requisições podem executar a mesma verificação e resultar em saldo negativo.

## Objetivos de Aprendizagem
- Simular condições de corrida em operações de débito.
- Combinar múltiplos clientes simultâneos contra o mesmo endpoint.
- Observar o impacto da falta de bloqueio pessimista.

## Serviços Disponíveis
- `GET /api/state` — Retorna o saldo atual das contas (`checking`, `credit`).
- `POST /api/withdraw` — Permite saques sem sincronização adequada.
- `GET /flag` — Retorna a flag quando `checking` fica negativo.

## Como Executar
1. Inicie o container.
2. Planeje saques de valor alto (ex.: 1000).
3. Dispare duas ou mais requisições simultâneas.

## Como Capturar a Flag
- Envie duas requisições `POST /api/withdraw` com `{"amount": 1000}` ao mesmo tempo.
- O saldo cairá para -500 e `/flag` retornará a flag.
