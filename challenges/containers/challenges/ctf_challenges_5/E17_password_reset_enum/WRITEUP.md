# Writeup — Redefinição Generosa

1. Inicie o fluxo de redefinição fornecendo um ID de usuário conhecido e observe a resposta.
2. Alterne o parâmetro `user_id` sequencialmente, anotando quais IDs retornam mensagens diferentes (por exemplo, confirmação de envio de e-mail ou link direto).
3. Quando localizar um ID privilegiado, capture o link de redefinição completo retornado na resposta.
4. Acesse o link, defina uma nova senha ou utilize o token de reset fornecido para autenticar-se como o usuário privilegiado.
5. Após o login, vá até o painel protegido e colete a flag `ITAU2025{reset_enum_abuse}`.

## Lições
- Fluxos de recuperação não devem indicar se um usuário existe.
- Tokens de reset precisam ser vinculados à conta correta e expirar rapidamente.
- Implementar rate limiting reduz risco de enumeração automatizada.
