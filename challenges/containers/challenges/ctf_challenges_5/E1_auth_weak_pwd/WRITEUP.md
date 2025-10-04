# Writeup — Sessão Reutilizável

1. Inicie a instância e acesse a URL individual fornecida.
2. Teste credenciais padrão comuns (por exemplo, `admin:admin`, `admin:password`, `root:root`). Caso não funcionem, enumere senhas triviais combinando o usuário sugerido pela interface com senhas simples.
3. Após autenticar-se, capture o token interno exibido pela aplicação ou retornado em JSON.
4. Envie o token para o endpoint indicado no painel (geralmente `/internal/flag` ou caminho similar) para validar o acesso.
5. Receba a flag `ITAU2025{weak_passwords_ruin_security}` na resposta do endpoint protegido.

## Lições
- Nunca deixe credenciais padrão ativas em produção.
- Implemente bloqueios progressivos e monitoramento de tentativas mal-sucedidas.
- Valide tokens de sessão e diferencie-os da flag definitiva para evitar confusões durante o fluxo de autenticação.
