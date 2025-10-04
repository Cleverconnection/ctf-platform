# Writeup — Relatório Aberto

1. Envie um filtro inofensivo (por exemplo, `branch=Central`) para verificar a estrutura de resposta.
2. Teste injeções simples como `'` para identificar erros SQL e confirmar vulnerabilidade.
3. Determine o número de colunas usando `ORDER BY` incremental ou `UNION SELECT NULL` repetido até a consulta funcionar.
4. Use `UNION SELECT` para recuperar informações úteis, como tabelas (`sqlite_master`) ou tokens armazenados em colunas sensíveis.
5. Quando identificar o token correto, acesse o endpoint indicado e obtenha a flag `ITAU2025{sqli_in_the_branch}`.

## Lições
- Utilize prepared statements em vez de concatenar strings em consultas SQL.
- Limite privilégios da conta do banco para minimizar impacto de injeções.
- Monitore erros e padrões incomuns em parâmetros de consulta.
