# Consulta por Identificador

**Categoria:** Web

## Cenário
Um serviço de contas expõe um endpoint de consulta por identificador numérico. Sem checagem de posse do recurso, basta variar o ID para obter dados de contas alheias.

## Recursos
- URL de acesso individual fornecida ao iniciar a instância do desafio.

## Objetivo
Identificar um ID de conta privilegiada e, a partir dos dados expostos, recuperar a flag.

## Flag
`ITAU2025{idor_bank_accounts}`

## Dica
IDs são previsíveis; compare respostas e procure campos extras em contas de alto nível.
