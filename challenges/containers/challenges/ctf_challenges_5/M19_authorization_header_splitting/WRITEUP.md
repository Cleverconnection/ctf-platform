# Write-up — M19 Quebra de Cabeçalho Authorization

## Visão Geral do Vetor
O backend divide o valor após `"Token "` usando `;` e aceita múltiplos pares `chave=valor`. Como não há validação de origem para `role`, basta enviar `role=admin` junto do token válido para receber a flag.

## Passo a Passo
1. `curl -H "Authorization: Token token=svc-ops-2025" http://localhost:8080/api/secure` para ver a resposta padrão (sem flag).
2. Repetir incluindo `;role=admin`.
3. Receber JSON com `status=ok`, `role=admin` e `flag`.

## Evidências
- Captura das duas respostas comparando os campos.
- Log da aplicação mostrando parsing dos campos do header.

## Mitigações Recomendadas
- Usar formatos padrão de autorização (Bearer, Basic) e evitar múltiplos parâmetros livres.
- Validar roles e outros atributos apenas no servidor, ignorando valores enviados pelo cliente.
- Implementar assinaturas ou tokens de acesso robustos (JWT, OAuth) ao invés de headers customizados.
