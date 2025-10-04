# Writeup — Compartilhamento Cruzado

1. Faça uma requisição direta à API e observe os cabeçalhos `Access-Control-Allow-Origin` e `Access-Control-Allow-Credentials`.
2. Crie uma página HTML maliciosa em seu ambiente (ou use ferramentas como `curl` com cabeçalho `Origin`) para simular uma origem externa.
3. Carregue a página em um navegador autenticado na aplicação e execute JavaScript que faça `fetch` para a API, incluindo `credentials: 'include'`.
4. Se a resposta for entregue à página externa, extraia o token ou informação sensível retornada.
5. Utilize o token obtido no endpoint indicado para recuperar a flag `ITAU2025{cors_wildcard_token}`.

## Lições
- Restrinja CORS a origens confiáveis e evite `*` quando cookies ou credenciais são utilizadas.
- Desabilite `Access-Control-Allow-Credentials` sempre que possível.
- Valide requisições no lado do servidor com autenticação forte e CSRF tokens.
