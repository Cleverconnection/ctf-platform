# Redefinição Generosa

**Categoria:** Web

## Cenário
Um fluxo de redefinição aceita identificadores numéricos e retorna links de reset sem validar a posse da conta. IDs previsíveis permitem descobrir usuários privilegiados.

## Recursos
- URL de acesso individual fornecida ao iniciar a instância do desafio.

## Objetivo
Enumerar identificadores até obter um link de reset privilegiado e usá-lo para alcançar a flag.

## Flag
`ITAU2025{reset_enum_abuse}`

## Dica
Observe mensagens distintas para IDs existentes vs. inexistentes e siga o link de reset.
