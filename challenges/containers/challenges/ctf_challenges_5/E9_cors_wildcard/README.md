# Compartilhamento Cruzado

**Categoria:** Web

## Cenário
Uma API foi publicada com configuração CORS permissiva, permitindo que páginas externas leiam respostas autenticadas do navegador do usuário.

## Recursos
- URL de acesso individual fornecida ao iniciar a instância do desafio.

## Objetivo
Demonstrar a leitura indevida e usar o artefato exposto para recuperar a flag.

## Flag
`ITAU2025{cors_wildcard_token}`

## Dica
Verifique cabeçalhos CORS e tente ler dados autenticados a partir de outra origem.
