# Writeup — Token Frágil

1. Gere um token legítimo com perfil básico através da aplicação e decodifique-o (geralmente Base64) para obter os blocos cifrados.
2. Identifique onde o campo de privilégio aparece no texto plano observando requisições de criação com diferentes perfis (por exemplo, `role=user`).
3. Gere outro token cujo payload coloque o valor desejado alinhado ao início de um bloco (por exemplo, preenchendo com padding até que `role=admin` comece exatamente em um bloco).
4. Faça cut-and-paste do bloco cifrado contendo `role=admin` no token original para construir um token híbrido.
5. Envie o token manipulado para o endpoint protegido e receba a flag `ITAU2025{weak_crypto_modes}`.

## Lições
- Modos de cifra sem IV aleatório ou MAC são vulneráveis a ataques de substituição de blocos.
- Utilize AES-GCM ou outra cifra autenticada para tokens sensíveis.
- Assine payloads com HMAC para detectar alterações.
