# Writeup — Download Genérico

1. Solicite um arquivo legítimo para entender o formato da requisição (por exemplo, `?path=public/manual.pdf`).
2. Altere o parâmetro `path` usando `../` ou caminhos absolutos (`/app/secret/flag.txt`) para escapar do diretório permitido.
3. Observe as respostas; mensagens de erro podem revelar caminhos reais do sistema.
4. Quando conseguir baixar o arquivo interno que contém o token ou a própria flag, salve seu conteúdo.
5. Se houver token intermediário, envie-o para o endpoint indicado e obtenha a flag `ITAU2025{file_download_traversal}`.

## Lições
- Endpoints de download devem validar e normalizar caminhos de arquivos.
- Implementar listas de permissão ou IDs abstratos evita exposição de estrutura interna.
- Restrinja permissões do sistema de arquivos para limitar o impacto de acessos indevidos.
