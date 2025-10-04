# Writeup — Leitor Amplo

1. Envie uma requisição para o leitor solicitando um arquivo existente (por exemplo, `?file=manual.txt`) para confirmar o formato de resposta.
2. Modifique o parâmetro utilizando sequências `../` até sair do diretório público: `?file=../flag.txt` ou `?file=../../flag.txt`.
3. Caso o caminho da flag não seja direto, liste arquivos sensíveis (como `../config/flag.txt` ou `../private/flag`) e ajuste o caminho conforme as mensagens de erro.
4. Quando o servidor retornar o conteúdo do arquivo protegido, copie a flag `ITAU2025{path_traversal_master}`.

## Lições
- Normalização de caminho e whitelists são fundamentais para operações de I/O.
- Controles adicionais como `chroot` e permissões limitadas reduzem impacto de travessia de diretórios.
- Logs devem registrar parâmetros suspeitos contendo `../`.
