# Writeup — Link Compartilhado

1. Navegue pela página inicial em busca de links externos ou botões de download contendo parâmetros de query.
2. Identifique o link com o parâmetro `token` e copie o valor fornecido.
3. Acesse diretamente a URL completa (ou utilize `curl`) para baixar o arquivo ou JSON protegido.
4. Extraia do conteúdo baixado o token ou a flag. Se retornar apenas um token, envie-o para o endpoint indicado para receber a flag `ITAU2025{creds_in_query}`.

## Lições
- Tokens sensíveis não devem ser compartilhados em query strings expostas.
- Links temporários precisam expirar rapidamente e exigir autenticação adicional.
- Registre e invalide tokens reutilizados por tempo excessivo.
