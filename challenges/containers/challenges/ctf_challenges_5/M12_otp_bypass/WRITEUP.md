# Write-up — M12 Bypass de OTP Previsível

## Visão Geral do Vetor
A função `calc_otp` multiplica os últimos 6 dígitos da conta por 3 e aplica módulo 1.000.000. Esse algoritmo é determinístico e a API fornece a dica com os últimos dígitos, tornando trivial calcular o valor completo.

## Passo a Passo
1. Solicitar `POST /api/send` com `{ "account": "98765432100" }`.
2. Identificar que a dica termina com `30`, confirmando os cálculos.
3. Calcular manualmente ou via script `calc = (543210 * 3) % 1000000 = 629630`.
4. Enviar `POST /api/verify` com o OTP calculado.
5. Receber resposta com a flag.

## Evidências
- Logs mostrando a chamada `verify` com status `ok`.
- Resposta JSON contendo `flag`.

## Mitigações Recomendadas
- Utilizar algoritmos OTP baseados em tempo (TOTP/HOTP) com segredos por usuário.
- Não divulgar dicas que revelem parte do código.
- Implementar bloqueio/ rate limit após tentativas erradas.
