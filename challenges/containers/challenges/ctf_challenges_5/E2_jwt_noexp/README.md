# Chave Persistente

**Categoria:** Web

## Cenário
Uma API interna emite tokens JWT para aplicações de backoffice sem expiração adequada e com validações permissivas no payload. Tokens antigos continuam aceitos e campos de função influenciam privilégios de acesso.

## Recursos
- URL de acesso individual fornecida ao iniciar a instância do desafio.

## Objetivo
Obter um token válido, ajustar o payload para elevar privilégios e acessar o recurso protegido que expõe a flag.

## Flag
`ITAU2025{jwt_without_expiration}`

## Dica
Inspecione o token e o payload; há um campo de função sem expiração para explorar.
