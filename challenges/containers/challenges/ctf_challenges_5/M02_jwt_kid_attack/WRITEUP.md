# Write-up — M02 JWT kid Attack

## Visão Geral do Vetor
A validação do serviço depende do cabeçalho JWT. Se o cliente informar `alg=none`, o backend chama `jwt.decode` sem verificar a assinatura. Já para `HS256`, o backend procura a chave com base no `kid` em disco, mas retorna string vazia quando o arquivo não existe — o que, combinado com a ausência de verificação de integridade, permite forjar tokens. Ambas as abordagens concedem privilégios de administrador.

## Passo a Passo
1. **Extrair Token Base** — Capture o token exibido no `/` ou gere um novo com a biblioteca `pyjwt`.
2. **Forjar Cabeçalho** — Altere o cabeçalho para `{"alg":"none"}` e remonte o JWT com base64 sem assinatura.
3. **Modificar Payload** — Ajuste o corpo para `{"user":"auditor","admin":true}`.
4. **Enviar Requisição** — Faça `GET /api/admin` com o header `Authorization: Bearer <token_modificado>`.
5. **Receber Flag** — A resposta retorna `flag` ao detectar `admin=true`.

_Alternativa:_ gerar assinatura com `HS256` usando o conteúdo de `keys/legacy.key` (obtido via montagem do container ou pela própria aplicação) e manter `kid=legacy.key`.

## Evidências
- Registro do JWT modificado e resposta 200 com a flag.
- Logs do servidor sem erros de verificação de assinatura.

## Mitigações Recomendadas
- Desabilitar suporte ao algoritmo `none` no `jwt.decode` (`options={"verify_signature": True}`).
- Validar lista de `kid` permitidos ou usar JWKS assinados.
- Rotacionar chaves comprometidas e auditar acessos suspeitos.
