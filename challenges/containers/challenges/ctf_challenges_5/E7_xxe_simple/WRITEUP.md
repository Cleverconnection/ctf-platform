# Writeup — Importação XML

1. Envie um XML simples para entender o formato esperado (por exemplo, `<data><item>teste</item></data>`).
2. Acrescente um `DOCTYPE` declarando uma entidade externa, como `<!DOCTYPE data [ <!ENTITY secret SYSTEM "file:///etc/flag"> ]>`.
3. Utilize a entidade no corpo do XML (`<item>&secret;</item>`) e envie novamente para o serviço.
4. A resposta deve conter o conteúdo do arquivo referenciado; procure pelo token ou caminho indicado.
5. Use o segredo extraído para acessar o endpoint final e obtenha a flag `ITAU2025{xxe_into_core}`.

## Lições
- Configure parsers XML para desabilitar DTDs e entidades externas (XXE).
- Valide e sanitize arquivos importados antes de processá-los internamente.
- Utilize contêineres e permissões mínimas para limitar impacto de vazamentos de arquivos.
