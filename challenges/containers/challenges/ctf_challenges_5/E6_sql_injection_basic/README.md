# Relatório Aberto

**Categoria:** Web

## Cenário
Um gerador de relatórios monta consultas ao banco de dados concatenando strings com parâmetros fornecidos pelo usuário. Sem parametrização, é possível alterar a consulta original e extrair dados sensíveis.

## Recursos
- URL de acesso individual fornecida ao iniciar a instância do desafio.

## Objetivo
Injetar SQL para recuperar um token ou dado que permita obter a flag do serviço.

## Flag
`ITAU2025{sqli_in_the_branch}`

## Dica
Procure parâmetros refletidos em cláusulas `LIKE` e tente `UNION` com o número correto de colunas.
