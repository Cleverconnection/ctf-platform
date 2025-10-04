# Desafio M07 — Desserialização Insegura em Java

## Descrição
O Job Server Java aceita objetos serializados enviados em Base64 e assume que são instâncias da classe `TrustedEnvelope`. Não há validação de classes permitidas, permitindo carregar gadgets arbitrários presentes no classpath e atingir a ação `admin`.

## Objetivos de Aprendizagem
- Produzir payloads Java serializados (por exemplo com `ysoserial`).
- Entender o formato `application/x-java-serialized-object` codificado em Base64.
- Manipular o campo `action` da classe `TrustedEnvelope` para obter a flag.

## Serviços Disponíveis
- `POST /api/jobs` — Recebe `payload=<base64>` via formulário.
- `GET /flag` — Bloqueado diretamente, apenas retornado quando um envelope com `action=admin` é desserializado.
- Arquivos estáticos (`index.html`, `theme.css`) com instruções no tema Itaú.

## Como Executar
1. Compile o projeto com `./gradlew shadowJar` ou utilize o binário fornecido na imagem Docker (feito automaticamente).
2. Gere um objeto `TrustedEnvelope` com `action=admin` e serialize-o usando um script Java ou `ysoserial` customizado.
3. Codifique o resultado em Base64 e envie via `curl -d "payload=<base64>"` para `/api/jobs`.

## Como Capturar a Flag
- Criar manualmente uma instância de `TrustedEnvelope("admin", "qualquer")`, serializar e enviar.
- O servidor reconhecerá a classe e retornará diretamente a flag na resposta HTTP.
