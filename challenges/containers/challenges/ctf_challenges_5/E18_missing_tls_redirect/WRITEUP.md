# Writeup — Transporte Opcional

1. Acesse o serviço explicitamente via `http://` (sem TLS) usando navegador ou `curl`.
2. Observe se cookies de sessão ou tokens são enviados sem os atributos `Secure` e `HttpOnly`.
3. Capture a resposta ou utilize ferramentas como `mitmproxy` para interceptar o tráfego em claro.
4. Reutilize o cookie/token coletado em uma requisição autenticada (preferencialmente por HTTPS) para acessar o endpoint protegido.
5. Receba a flag `ITAU2025{tls_redirect_missing}`.

## Lições
- Forçar redirecionamento automático para HTTPS impede vazamento por links inseguros.
- Cookies de sessão devem ter atributos `Secure` e `HttpOnly`.
- Utilize HSTS para instruir navegadores a evitar conexões HTTP.
