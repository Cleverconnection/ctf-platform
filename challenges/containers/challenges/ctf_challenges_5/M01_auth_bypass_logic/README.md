# Desafio M01 — Auth Bypass Logic

## Descrição
O time antifraude construiu um fluxo de autenticação em três etapas (senha → MFA → conclusão), mas confiou apenas no campo `step` enviado pelo cliente na etapa final. O objetivo do desafio é reproduzir a falha de lógica de negócios e conseguir uma sessão privilegiada sem completar o MFA legítimo.

## Objetivos de Aprendizagem
- Identificar validações de estado frágeis em fluxos multi-etapas.
- Manipular chamadas de API observando o contrato JSON exposto pelo front-end.
- Entender como verificar respostas para confirmar a exposição da flag.

## Serviços Disponíveis
- `GET /` — Interface web com documentação simplificada do fluxo.
- `POST /api/start` — Valida usuário e senha, retorna `session_id`.
- `POST /api/mfa` — Verifica token MFA e atualiza o estado esperado.
- `POST /api/complete` — Conclui o login com base apenas no valor de `step` informado pelo cliente.
- `GET /flag` — Não existe; a flag só é retornada quando o fluxo é concluído.

## Como Executar
1. Faça `docker compose up` dentro da pasta do desafio ou utilize o `make run` global do projeto.
2. Acesse `http://localhost:8080` para inspecionar o fluxo sugerido pela equipe de produto.
3. Use ferramentas como cURL, Postman ou o console do navegador para interagir com os endpoints REST.

## Como Capturar a Flag
- Inicie uma sessão válida com `POST /api/start` usando `{"username":"analyst","password":"senh@F0rte"}`.
- Pule o passo MFA enviando diretamente `POST /api/complete` com o mesmo `session_id` e `{"step":"mfa_ok"}`.
- A resposta conterá o campo `flag`, confirmando o bypass bem-sucedido.
