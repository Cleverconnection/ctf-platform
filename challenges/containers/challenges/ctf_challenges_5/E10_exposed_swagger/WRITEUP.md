# Writeup — Manual Público

1. Acesse a interface Swagger disponível na URL fornecida e abra o arquivo `swagger.json`.
2. Analise os campos `securitySchemes` ou parâmetros com valores `example` ou `default`; frequentemente contêm tokens reais ou credenciais básicas.
3. Use as próprias ferramentas da interface para testar a rota interna mencionada na documentação (por exemplo, `/internal/flag`).
4. Inclua o token ou header encontrado nos exemplos ao executar a requisição.
5. Receba a resposta com a flag `ITAU2025{swagger_spill}`.

## Lições
- Documentação pública não deve expor segredos reais ou ambientes internos.
- Desabilite a execução interativa em ambientes externos e proteja a interface com autenticação.
- Faça revisões periódicas nos exemplos antes de publicar documentos técnicos.
