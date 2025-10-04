# Writeup — Consulta por Identificador

1. Acesse a URL do serviço e faça uma requisição com o ID sugerido pela interface para entender o formato de resposta.
2. Altere o parâmetro `id` sequencialmente (por exemplo, `?id=1`, `?id=2`...) até localizar uma conta com campos adicionais como `role`, `tier` ou um caminho para a flag.
3. Assim que encontrar a conta privilegiada, copie o valor do campo indicado (token, caminho ou URL secundária).
4. Utilize o artefato fornecido para consultar o endpoint protegido e recuperar a flag `ITAU2025{idor_bank_accounts}`.

## Lições
- Falta de checagem de autorização por objeto (IDOR) leva à exposição de dados críticos.
- IDs previsíveis precisam de controles adicionais, como UUIDs ou verificações de proprietário.
- Logs e monitoramento devem detectar acessos fora do perfil esperado.
