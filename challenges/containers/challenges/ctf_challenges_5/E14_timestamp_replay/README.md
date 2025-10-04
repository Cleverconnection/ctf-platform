# Transação Repetida

**Categoria:** Web

## Cenário
O motor de transações aceita o mesmo timestamp diversas vezes dentro de uma janela, acumulando créditos.

## Recursos
- URL de acesso individual fornecida ao iniciar a instância do desafio.

## Objetivo
Repetir a mesma transação de forma controlada até acionar o retorno que libera a flag.

## Flag
`ITAU2025{timestamp_replay_attack}`

## Dica
Repita a requisição com o mesmo timestamp até atingir o gatilho.
