# Write-up — M06 XML DoS + XXE

## Visão Geral do Vetor
O parser `lxml.etree` está configurado com `resolve_entities=True`, `load_dtd=True` e `no_network=False`, aceitando DTDs arbitrárias. Isso habilita tanto ataques de negação de serviço (expansão de entidades) quanto a leitura de recursos HTTP internos. A flag pode ser extraída referenciando o endpoint `/flag` via entidade externa.

## Passo a Passo
1. Prepare o XML com DTD inline que define `<!ENTITY flag SYSTEM "http://127.0.0.1:8080/flag">`.
2. Envie o payload para `/api/import` utilizando `curl --data-binary @payload.xml`.
3. A resposta JSON trará o campo `echo` com o conteúdo retornado pelo endpoint referenciado, incluindo `ITAU2025{...}`.

## Evidências
- Captura do request/resposta mostrando o XML retornado com a flag.
- Logs de acesso indicando requisição interna ao endpoint `/flag` feita pelo servidor.

## Mitigações Recomendadas
- Desabilitar completamente a resolução de entidades externas (`resolve_entities=False`).
- Utilizar parsers seguros (ex.: `defusedxml`).
- Filtrar e validar o conteúdo antes do processamento, aplicando limites de tamanho para evitar DoS.
