# Write-up — M18 Exposição de Armazenamento de Arquivos

## Visão Geral do Vetor
O código forma o caminho final com `BASE_DIR / name` sem qualquer validação. Fornecendo `private/flag.txt`, o path resultante aponta para o diretório privado e o conteúdo é retornado diretamente.

## Passo a Passo
1. Testar com `GET /api/file?path=public/notice.txt` para confirmar funcionamento.
2. Solicitar `GET /api/file?path=private/flag.txt`.
3. Ler a flag no campo `content` da resposta.

## Evidências
- Requisição HTTP e resposta contendo a flag.
- Logs de acesso revelando leitura do arquivo privado.

## Mitigações Recomendadas
- Restringir o acesso a uma allowlist de diretórios autorizados.
- Implementar checagens para evitar path traversal e subdiretórios sensíveis.
- Armazenar segredos fora do diretório servido publicamente.
