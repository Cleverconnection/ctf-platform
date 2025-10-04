# Write-up — M08 Vazamento em Pipeline DevOps

## Visão Geral do Vetor
O backend expõe diretamente o diretório `artifacts/` sem autenticação. O job `ensure_artifact()` escreve a flag no arquivo `runner.log`, que fica disponível via `GET /artifact/runner.log`.

## Passo a Passo
1. Requisitar `/api/pipelines/latest` para confirmar o caminho do artefato.
2. Baixar `http://localhost:8080/artifact/runner.log`.
3. Ler a linha `Secret token: ITAU2025{...}` no conteúdo retornado.

## Evidências
- Resposta 200 contendo o log completo com a flag.
- Registro do servidor mostrando `GET /artifact/runner.log` sem autenticação.

## Mitigações Recomendadas
- Forçar autenticação e autorização antes de expor artefatos.
- Separar logs internos de arquivos distribuídos a clientes.
- Sanitizar informações sensíveis em logs ou substituí-las por identificadores temporários.
