# Transporte Opcional

**Categoria:** Web

## Cenário
Um serviço opera simultaneamente em HTTP e HTTPS sem forçar redirecionamento seguro. Sessões e dados podem transitar em claro quando acessados sem TLS.

## Recursos
- URL de acesso individual fornecida ao iniciar a instância do desafio.

## Objetivo
Capturar informações de sessão acessando o serviço de forma não cifrada e utilizá-las para recuperar a flag.

## Flag
`ITAU2025{tls_redirect_missing}`

## Dica
Acesse via HTTP simples e verifique cookies ou JSON de sessão.
