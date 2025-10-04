# Writeup — Registros Não Confiáveis

1. Submeta mensagens pelo painel e visualize o log para entender o formato armazenado.
2. Identifique qual marcador o processo de verificação espera (por exemplo, `status=approved`). Essa pista costuma aparecer em mensagens de erro ou dicas.
3. Envie uma nova entrada contendo o marcador exato, possivelmente acrescentando quebras de linha (`\n`) ou separadores se o formato exigir.
4. Acesse novamente a visualização do log para confirmar que a entrada foi registrada exatamente como enviado.
5. Acione o verificador ou endpoint que lê o log; ele encontrará o marcador injetado e retornará a flag `ITAU2025{logs_are_trust_issue}`.

## Lições
- Logs não devem confiar em entradas de usuários sem sanitização.
- Use delimitadores claros e escape de caracteres especiais ao escrever em arquivos.
- Processos que consomem logs precisam validar origem e formato dos eventos.
