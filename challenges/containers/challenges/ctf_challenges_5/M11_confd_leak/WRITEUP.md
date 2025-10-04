# Write-up — M11 Vazamento em Endpoint de Configuração

## Visão Geral do Vetor
O endpoint `/api/config/<env>` simplesmente retorna o dicionário `CONFIGS[env]`. O ambiente `prod` inclui um objeto `secrets` com a flag. Não há autenticação nem filtragem baseada no chamador.

## Passo a Passo
1. `GET /api/config/dev` para mapear a estrutura.
2. `GET /api/config/prod`.
3. Ler o JSON de resposta e copiar o valor `config.secrets.flag`.

## Evidências
- Registro HTTP mostrando a chamada a `prod` e o JSON com a flag.

## Mitigações Recomendadas
- Exigir autenticação forte para APIs de configuração.
- Segmentar segredos, servindo-os apenas a serviços autorizados (mTLS, IAM).
- Implementar mascaramento de campos sensíveis em respostas.
