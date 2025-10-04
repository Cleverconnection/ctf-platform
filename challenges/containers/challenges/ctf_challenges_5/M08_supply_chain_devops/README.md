# Desafio M08 — Vazamento em Pipeline DevOps

## Descrição
O simulador de pipeline CI/CD publica artefatos gerados pela última execução em um diretório acessível. O arquivo `runner.log` contém informações operacionais e, por engano, um segredo sensível exposto pelo script de build.

## Objetivos de Aprendizagem
- Enumerar endpoints de distribuição de artefatos.
- Baixar logs de execução para buscar segredos.
- Compreender os riscos de exposição de pipelines e runners.

## Serviços Disponíveis
- `GET /api/pipelines/latest` — Retorna metadados sobre a execução mais recente.
- `GET /artifact/runner.log` — Disponibiliza o log com a flag embutida.
- `GET /` — Painel com orientação ao analista.

## Como Executar
1. Levante o container do desafio.
2. Consulte `/api/pipelines/latest` para descobrir o caminho do artefato.
3. Faça download do arquivo informado utilizando navegador ou `curl`.

## Como Capturar a Flag
- Acesse diretamente `GET /artifact/runner.log` e leia a linha `Secret token`, que carrega a flag do desafio.
