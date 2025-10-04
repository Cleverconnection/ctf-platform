# Writeup — Envio Público

1. Utilize a funcionalidade de upload para enviar um arquivo teste e note o padrão de nomenclatura (por exemplo, timestamps ou hashes previsíveis).
2. Use o mesmo padrão para enumerar arquivos vizinhos acessando URLs sequenciais ou alfabeticamente próximas.
3. Procure arquivos listados contendo palavras-chave como `flag`, `secret` ou `proof`.
4. Ao localizar o arquivo sensível, acesse-o diretamente pelo servidor HTTP e copie a flag `ITAU2025{predictable_upload_leak}`.

## Lições
- Armazene uploads em diretórios isolados e com nomes imprevisíveis.
- Não mantenha documentos internos na mesma raiz acessível publicamente.
- Implemente autenticação e autorização para áreas administrativas de upload.
