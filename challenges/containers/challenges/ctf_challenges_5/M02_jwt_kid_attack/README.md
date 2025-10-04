# Desafio M02 — JWT kid Attack

## Descrição
A API de autorização assina tokens JWT usando chaves simétricas e confia no cabeçalho `kid` informado pelo cliente para escolher qual arquivo carregar. Além disso, ela aceita o algoritmo `none` quando o cabeçalho o declara, permitindo tokens sem assinatura. Explore a confusão de chaves para assumir privilégios administrativos.

## Objetivos de Aprendizagem
- Investigar cabeçalhos JWT (`kid`, `alg`) e compreender como manipulá-los.
- Forjar tokens usando o modo `none` ou apontar `kid` para arquivos controlados.
- Validar o ganho de privilégios acessando o endpoint administrativo protegido.

## Serviços Disponíveis
- `GET /` — Interface que mostra um token de exemplo.
- `GET /api/admin` — Exige token JWT via `Authorization: Bearer <token>` e expõe a flag quando `admin=true`.
- `GET /health` — Verificação de integridade.

## Como Executar
1. Suba o container com `docker compose up` nesta pasta.
2. Copie o token demonstrado na interface ou gere um novo com bibliotecas JWT.
3. Manipule o cabeçalho JWT conforme descrito nos objetivos.

## Como Capturar a Flag
- Gere um token com payload `{"user":"auditor","admin":true}` e cabeçalho `{"alg":"none"}`; não é necessário assinar.
- Como alternativa, utilize `HS256` e defina `kid` para apontar para `keys/legacy.key`, assinando com o conteúdo do arquivo.
- Envie o token em `Authorization: Bearer <jwt>` para `/api/admin` e receba a flag em caso de sucesso.
