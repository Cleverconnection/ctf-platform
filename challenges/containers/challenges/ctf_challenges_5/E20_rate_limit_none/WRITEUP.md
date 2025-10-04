# Writeup — Validador Infinito

1. Identifique o formato do código solicitado (por exemplo, 4 dígitos numéricos) observando mensagens de erro.
2. Crie um script simples que itere por todas as combinações possíveis e envie requisições rápidas ao endpoint.
3. Como não há rate limiting, mantenha o ritmo das requisições até que o serviço responda com sucesso.
4. A resposta bem-sucedida geralmente contém a flag diretamente ou um token final.
5. Registre a flag `ITAU2025{rate_limit_none}`.

## Lições
- Implementar rate limiting e bloqueios progressivos é fundamental para códigos temporários.
- Aumentar a entropia dos códigos reduz a viabilidade de força bruta.
- Monitore padrões de tentativas para detectar ataques automatizados.
