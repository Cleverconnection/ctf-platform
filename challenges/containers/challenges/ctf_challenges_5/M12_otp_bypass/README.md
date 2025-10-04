# Desafio M12 — Bypass de OTP Previsível

## Descrição
O serviço de autenticação gera códigos OTP a partir dos dígitos finais da conta e ainda retorna uma dica com os dois últimos dígitos, tornando o código facilmente dedutível.

## Objetivos de Aprendizagem
- Identificar geradores de OTP determinísticos.
- Utilizar dicas e padrões expostos pela API para reconstruir o token completo.
- Automatizar tentativas com base no algoritmo observado.

## Serviços Disponíveis
- `POST /api/send` — Envia (simulado) o OTP e retorna dica dos últimos dígitos.
- `POST /api/verify` — Valida o OTP informado.
- `GET /` — Interface com contexto do desafio.

## Como Executar
1. Suba o container do desafio.
2. Chame `/api/send` com a conta informada para obter a dica.
3. A partir da lógica deduzida, calcule o OTP completo.

## Como Capturar a Flag
- O algoritmo é `otp = ((int(identificador[-6:]) * 3) % 1000000)`.
- Para a conta `98765432100`, o valor é `((543210 * 3) % 1000000) = 629630`.
- Envie `POST /api/verify` com `{"account":"98765432100","otp":"629630"}` e receba a flag.
