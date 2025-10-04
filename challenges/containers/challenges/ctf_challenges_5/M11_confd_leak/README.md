# Desafio M11 — Vazamento em Endpoint de Configuração

## Descrição
Um endpoint de configuração pensado para uso interno expõe configurações de todos os ambientes, incluindo chaves e a flag no ambiente de produção.

## Objetivos de Aprendizagem
- Enumerar ambientes suportados em APIs de configuração.
- Reconhecer objetos com segredos aninhados.
- Valorizar a segmentação de dados sensíveis por ambiente.

## Serviços Disponíveis
- `GET /api/config/<env>` — Retorna configurações para `dev`, `prod`, etc.
- `GET /` — Interface descritiva.

## Como Executar
1. Suba o serviço do desafio.
2. Consulte `/api/config/dev` para ver a estrutura retornada.
3. Troque o parâmetro para `prod`.

## Como Capturar a Flag
- A resposta de `/api/config/prod` contém `config.secrets.flag` com o valor da flag.
