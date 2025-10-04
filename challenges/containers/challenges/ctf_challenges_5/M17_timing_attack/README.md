# Desafio M17 — Ataque por Timing em Autenticação

## Descrição
A API de login compara senha caractere por caractere e insere um atraso a cada caractere correto. Isso permite inferir a senha por medição de tempo, além de confirmar se o usuário existe.

## Objetivos de Aprendizagem
- Medir tempos de resposta para deduzir strings protegidas.
- Automatizar brute force baseado em timing.
- Entender a importância de comparações em tempo constante.

## Serviços Disponíveis
- `POST /api/login` — Recebe `username` e `password`, retornando flag ao acertar `executivo`/`9246`.
- `GET /` — Interface explicativa.

## Como Executar
1. Suba o container.
2. Utilize scripts que enviem tentativas de senha medindo o tempo (por exemplo, `time.perf_counter()` em Python).
3. Determine o usuário correto e descubra a senha um caractere por vez.

## Como Capturar a Flag
- Note que o usuário válido é `executivo`.
- Medindo o tempo, identifique que cada caractere correto adiciona ~120ms. Descubra `9246`.
- Envie `POST /api/login` com as credenciais corretas para obter a flag.
