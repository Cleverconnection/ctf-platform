# Writeup — Requisição Transparente

1. Utilize o parâmetro de URL do proxy para fazer uma requisição simples a um domínio público e confirmar o comportamento.
2. Substitua o destino pela URL interna desejada, como `http://127.0.0.1:8000/internal` ou outra porta que apareça em mensagens de erro.
3. Interprete a resposta retornada pelo proxy; serviços internos geralmente respondem com JSON contendo o token ou a própria flag.
4. Se necessário, experimente diferentes portas internas (`8000`, `8080`, `5000`) até encontrar a que hospeda o endpoint protegido.
5. Ao acessar o recurso correto, obtenha a flag `ITAU2025{ssrf_proxy_to_flag}`.

## Lições
- Proxies devem validar destinos e restringir o acesso a redes internas.
- Implementar listas de permissão e filtrar esquemas/hosts evita SSRF.
- Monitorar requisições inesperadas pode identificar abuso rapidamente.
