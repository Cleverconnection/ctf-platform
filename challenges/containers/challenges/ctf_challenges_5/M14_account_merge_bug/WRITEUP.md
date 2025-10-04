# Write-up — M14 Vazamento em Fusão de Contas

## Visão Geral do Vetor
O endpoint `/api/merge` usa `deepcopy` da conta primária e retorna o objeto secundário inteiro como parte da resposta. Como a conta `7777` tem a flag em `notes`, qualquer fusão que a envolva expõe a informação.

## Passo a Passo
1. Identificar `primary=1001`, `secondary=7777` via `/api/accounts`.
2. Executar `POST /api/merge` com o JSON `{ "primary": "1001", "secondary": "7777" }`.
3. Ler a resposta e capturar o campo `merged.secondary.notes` contendo a flag.

## Evidências
- Corpo de resposta exibindo a flag.
- Logs da aplicação confirmando a remoção da conta `7777` após a fusão.

## Mitigações Recomendadas
- Retornar apenas dados estritamente necessários após operações de fusão.
- Definir políticas de mascaramento para campos sensíveis.
- Exigir permissões elevadas para operações que envolvem contas privilegiadas.
