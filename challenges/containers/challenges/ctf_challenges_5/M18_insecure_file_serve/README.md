# Desafio M18 — Exposição de Armazenamento de Arquivos

## Descrição
A API de download concatena o caminho solicitado diretamente ao diretório base e lê o arquivo resultante sem validar se está em `storage/public`. Isso permite acessar arquivos privados contendo a flag.

## Objetivos de Aprendizagem
- Explorar exposições de armazenamento tipo object storage.
- Entender os riscos de confiar em caminhos fornecidos pelo cliente.
- Navegar por diretórios internos sem sanitização.

## Serviços Disponíveis
- `GET /api/file?path=` — Retorna o conteúdo do arquivo solicitado.
- Estrutura de diretórios `storage/public` e `storage/private`.

## Como Executar
1. Inicie o container.
2. Solicite `GET /api/file?path=public/notice.txt` para testar o endpoint.
3. Modifique o parâmetro para acessar arquivos privados.

## Como Capturar a Flag
- Requisite `GET /api/file?path=private/flag.txt`.
- O JSON retornará o conteúdo do arquivo com a flag.
