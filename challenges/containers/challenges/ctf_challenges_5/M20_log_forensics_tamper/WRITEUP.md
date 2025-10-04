# Write-up — M20 Manipulação de Logs Forenses

## Visão Geral do Vetor
A aplicação grava mensagens fornecidas pelo cliente diretamente no arquivo `audit.log` e permite exportar o conteúdo sem qualquer verificação. Como o arquivo já contém a flag, basta lê-la; adicionalmente, é possível encobrir rastros inserindo mensagens enganosas.

## Passo a Passo
1. `GET /api/logs` para listar as últimas linhas — observe `vault;flag;ITAU2025{...}`.
2. Opcionalmente, `POST /api/logs/write` com uma mensagem personalizada para adicionar ruído.
3. `GET /api/logs/export` e abra `audit.log` dentro do ZIP para confirmar a manipulação e a presença da flag.

## Evidências
- Arquivo `audit.log` exportado contendo a flag e quaisquer entradas falsas adicionadas.

## Mitigações Recomendadas
- Tornar logs somente append por processos autenticados, assinando cada linha (hash encadeado).
- Restringir a API de escrita a operações autenticadas e auditadas.
- Monitorar alterações em logs críticos com trilhas de auditoria imutáveis.
