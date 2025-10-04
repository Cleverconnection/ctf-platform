# Desafio M03 — SSRF em Serviço Interno

## Descrição
Uma ferramenta de monitoramento permite ao analista "verificar URLs suspeitas" e encaminha requisições para qualquer destino HTTP externo. O filtro de host é superficial e não bloqueia endereços alternativos da própria máquina, possibilitando alcançar um endpoint administrativo interno protegido por IP e cabeçalho secreto.

## Objetivos de Aprendizagem
- Explorar Server-Side Request Forgery (SSRF) em serviços proxy.
- Contornar listas de bloqueio simples para atingir `127.0.0.1` usando variantes (`127.1`, `localhost.localdomain`, etc.).
- Incluir cabeçalhos arbitrários e comprovar o acesso ao serviço interno.

## Serviços Disponíveis
- `GET /` — Interface de teste de URLs.
- `GET /api/fetch?url=` — Proxy inseguro que repassa o corpo da resposta.
- `GET /internal/ops` — Endpoint interno que só aceita chamadas locais com header `X-Internal-Key`.

## Como Executar
1. Suba o ambiente com `docker compose up` nesta pasta.
2. Faça requisições ao proxy usando o navegador ou cURL para observar os filtros.
3. Ajuste o parâmetro `url` até conseguir atingir o serviço interno.

## Como Capturar a Flag
- Chame `/api/fetch?url=http://127.1:8080/internal/ops&internal_key=svc-admin-2025`.
- O proxy executará a chamada localmente, adicionará o cabeçalho fornecido e retornará o JSON com a flag.
