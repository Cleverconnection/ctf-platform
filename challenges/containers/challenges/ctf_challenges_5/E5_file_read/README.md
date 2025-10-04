# Leitor Amplo

**Categoria:** Web

## Cenário
Um leitor de arquivos serve documentos a partir de um diretório base do container. Devido à concatenação direta de caminhos, é possível acessar arquivos fora do diretório previsto.

## Recursos
- URL de acesso individual fornecida ao iniciar a instância do desafio.

## Objetivo
Realizar travessia de diretórios para ler o arquivo de flag localizado fora da pasta pública.

## Flag
`ITAU2025{path_traversal_master}`

## Dica
Teste sequências com `../` para sair do diretório exposto.
