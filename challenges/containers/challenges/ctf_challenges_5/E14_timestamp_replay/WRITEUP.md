# Writeup — Transação Repetida

1. Envie uma transação legítima e capture os parâmetros, especialmente o `timestamp`.
2. Reenvie a mesma requisição múltiplas vezes dentro da janela aceita pelo serviço, mantendo exatamente o mesmo timestamp.
3. Monitore as respostas até que o serviço indique que o limite foi ultrapassado ou que créditos extras foram acumulados.
4. Quando o gatilho for ativado, o serviço retorna diretamente a flag ou fornece um token adicional.
5. Registre a flag `ITAU2025{timestamp_replay_attack}`.

## Lições
- Use nonces ou identificadores únicos para cada transação sensível.
- Rejeite timestamps repetidos e aplique rate limiting por origem.
- Registre tentativas repetidas para detectar comportamentos anômalos.
