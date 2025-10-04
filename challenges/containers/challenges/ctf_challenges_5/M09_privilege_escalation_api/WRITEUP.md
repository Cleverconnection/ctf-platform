# Write-up — M09 Escalada de Privilégio em API

## Visão Geral do Vetor
A função `update()` aceita tanto objetos quanto strings para o campo `role`. Quando recebe uma string, o backend sobrescreve `user["role"]` com esse valor sem qualquer validação. Basta enviar `{"role": "admin"}` para se tornar administrador.

## Passo a Passo
1. `GET /api/users/me` para coletar o estado inicial.
2. `PATCH /api/users/me` com corpo `{"role":"admin"}` e header `Content-Type: application/json`.
3. Receber resposta `{"status":"ok","role":"admin"}`.
4. `GET /flag` e capturar a flag.

## Evidências
- Requisição PATCH retornando role `admin`.
- Requisição subsequente a `/flag` devolvendo `ITAU2025{...}`.

## Mitigações Recomendadas
- Validar tipos esperados com schemas (JSON Schema, Marshmallow etc.).
- Remover suporte legado inseguro ou encapsular as regras em DTOs.
- Aplicar controle de acesso baseado em servidor, ignorando atributos declarados pelo cliente.
