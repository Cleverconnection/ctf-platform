# Writeup — Chave Persistente

1. Solicite um token JWT por meio da URL do desafio e capture a resposta (geralmente JSON com `token`).
2. Decodifique o JWT usando uma ferramenta como `jwt.io` ou `python -m jwt` para visualizar cabeçalho e payload.
3. Observe que o campo `exp` está ausente e existe um claim de função/perfil. Edite o payload localmente para trocar o perfil por um valor privilegiado (por exemplo, `admin`).
4. Reassine o token reutilizando a mesma chave (se HS256, tente chave vazia ou obtenha a chave pública indicada na documentação). Com ausência de expiração, o servidor aceitará tokens antigos.
5. Envie o JWT modificado na requisição protegida indicada pela API para recuperar a flag `ITAU2025{jwt_without_expiration}`.

## Lições
- Tokens sem expiração comprometem a revogação e o controle de sessão.
- Claims sensíveis devem ser validados e assinados com chaves seguras.
- É essencial rotacionar chaves e auditar tokens long-lived.
