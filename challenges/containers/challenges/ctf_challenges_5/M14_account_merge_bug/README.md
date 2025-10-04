# Desafio M14 — Vazamento em Fusão de Contas

## Descrição
O processo de fusão de contas retorna tanto o registro primário atualizado quanto o registro secundário anexado. A conta VIP (`7777`) contém a flag nos campos de notas e acaba sendo devolvida ao cliente durante a fusão.

## Objetivos de Aprendizagem
- Avaliar respostas de APIs que retornam objetos complexos após operações.
- Explorar vazamentos decorrentes de junção de dados sensíveis.
- Compreender como copiar dados inadvertidamente entre contas.

## Serviços Disponíveis
- `GET /api/accounts` — Lista contas com dados públicos.
- `POST /api/merge` — Realiza fusão entre duas contas.
- `GET /flag` — Bloqueado; a flag só aparece via resposta do merge.

## Como Executar
1. Suba o container do desafio.
2. Consulte `/api/accounts` para identificar IDs disponíveis.
3. Realize `POST /api/merge` definindo `primary` como uma conta comum (ex.: `1001`) e `secondary` como `7777`.

## Como Capturar a Flag
- A resposta do merge inclui `"secondary": {"notes": "ITAU2025{...}"}`. Basta ler o JSON retornado.
