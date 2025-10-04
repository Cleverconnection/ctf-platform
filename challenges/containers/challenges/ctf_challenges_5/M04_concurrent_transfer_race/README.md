# Desafio M04 — Corrida em Transferências Concorrentes

## Descrição
O microserviço de transferências não usa bloqueios ao debitar e creditar contas distintas. Um atraso artificial (`sleep`) torna viável executar requisições simultâneas que leem o mesmo saldo inicial, resultando em débito incorreto e enriquecimento da conta de fraude.

## Objetivos de Aprendizagem
- Experimentar condições de corrida em APIs financeiras.
- Orquestrar múltiplas requisições paralelas para obter efeitos não determinísticos.
- Verificar estados intermediários e finais através do endpoint `/api/state`.

## Serviços Disponíveis
- `GET /` — Interface que apresenta o cenário e instruções.
- `GET /api/state` — Consulta saldos atuais das contas.
- `POST /api/transfer` — Realiza transferências sem sincronização.
- `GET /flag` — Disponibiliza a flag quando a conta `fraude` tiver ≥ 4000.

## Como Executar
1. Inicie o container localmente.
2. Utilize scripts com `requests`, `curl` paralelo ou ferramentas como `burp intruder`/`hey` para disparar dois POSTs simultâneos.
3. Monitore o saldo da conta `fraude` após cada tentativa.

## Como Capturar a Flag
- Envie duas transferências ao mesmo tempo retirando 3000 da conta `pagamentos` para `fraude`.
- Ambas as requisições enxergam saldo suficiente e creditarão 6000 no total, elevando `fraude` para ≥ 4000.
- Solicite `GET /flag` para receber a flag após o desvio.
