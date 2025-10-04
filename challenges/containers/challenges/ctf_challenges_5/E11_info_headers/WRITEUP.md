# Writeup — Cabeçalhos Reveladores

1. Faça uma requisição ao endpoint de healthcheck e inspecione os cabeçalhos de resposta, especialmente aqueles que começam com `X-`.
2. Identifique valores que pareçam caminhos ou URLs internas (por exemplo, `/internal/hint.txt`).
3. Solicite o recurso indicado pelos cabeçalhos; normalmente ele conterá um token intermediário ou instruções adicionais.
4. Siga as orientações até alcançar o endpoint final responsável por retornar a flag.
5. Recupere a flag `ITAU2025{headers_tell_secrets}`.

## Lições
- Cabeçalhos de diagnóstico devem ser limitados em ambientes de produção.
- Informações de caminho interno facilitam reconhecimento e movimentos laterais.
- Utilize logs e monitoramento para detectar acessos incomuns a rotas administrativas.
