# Write-up — M13 CSRF em API com Cookies

## Visão Geral do Vetor
O middleware CORS define `Access-Control-Allow-Origin: *` e `Allow-Credentials: true`, quebrando as recomendações do CORS. Com isso, qualquer site consegue enviar requisições autenticadas usando `fetch(..., { credentials: 'include' })`. O endpoint `/api/transfer` não exige token anti-CSRF.

## Passo a Passo
1. Visite `http://localhost:8080/` para obter o cookie de sessão.
2. Em outro domínio (ou no console dev, simulando origem diferente com `Origin` manual), execute o `fetch` mostrado no README.
3. Observe a resposta com `status: ok` e o campo `flag`.

## Evidências
- Resposta JSON exibindo a transferência para `shadow` com valor ≥ 1200.
- Cabeçalhos CORS permissivos na resposta (`Access-Control-Allow-Origin: *`).

## Mitigações Recomendadas
- Configurar CORS para permitir apenas origens confiáveis e, quando `Allow-Credentials=true`, especificar origem exata.
- Implementar tokens anti-CSRF ou exigir cabeçalhos customizados não acessíveis por sites externos.
- Utilizar `SameSite=Lax`/`Strict` para cookies sensíveis.
