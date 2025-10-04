# Desafio M20 — Manipulação de Logs Forenses

## Descrição
O sistema de auditoria permite ao operador registrar eventos arbitrários no log principal e exportá-lo em formato ZIP. A flag já está presente nos registros históricos, mas o desafio incentiva a manipular logs (inserir/alterar) antes de exportar para encobrir rastros.

## Objetivos de Aprendizagem
- Ler e interpretar logs históricos.
- Escrever entradas adicionais para mascarar eventos anteriores.
- Exportar o log completo para análise offline.

## Serviços Disponíveis
- `GET /api/logs` — Retorna as últimas linhas do log `audit.log`.
- `POST /api/logs/write` — Acrescenta uma nova linha com timestamp controlado pelo cliente.
- `GET /api/logs/export` — Gera um ZIP contendo todo o log.

## Como Executar
1. Inicie o container.
2. Use `/api/logs` para inspecionar o conteúdo inicial (já inclui a flag).
3. Opcionalmente, insira linhas falsas com `/api/logs/write` e depois exporte o log para verificar a manipulação.

## Como Capturar a Flag
- A flag está registrada em `audit.log`. Basta consultar `/api/logs` ou baixar `/api/logs/export` e localizar a linha `vault;flag`.
