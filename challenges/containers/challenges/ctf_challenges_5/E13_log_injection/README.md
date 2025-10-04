# Registros Não Confiáveis

**Categoria:** Web

## Cenário
Um painel operacional grava entradas do usuário diretamente em um arquivo de log. Sem sanitização, é possível injetar conteúdo tratado como evento válido por outros componentes.

## Recursos
- URL de acesso individual fornecida ao iniciar a instância do desafio.

## Objetivo
Injetar uma marcação controlada no log e utilizá-la para satisfazer a verificação que libera a flag.

## Flag
`ITAU2025{logs_are_trust_issue}`

## Dica
Envie uma entrada contendo um marcador `chave=valor` esperado pelo verificador.
