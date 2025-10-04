# Requisição Transparente

**Categoria:** Web

## Cenário
Um proxy de integrações busca conteúdo externo a partir de uma URL informada. Sem restrições de destino, o serviço pode ser induzido a consultar endereços internos da infraestrutura.

## Recursos
- URL de acesso individual fornecida ao iniciar a instância do desafio.

## Objetivo
Explorar o proxy para alcançar um endpoint interno protegido e obter a flag.

## Flag
`ITAU2025{ssrf_proxy_to_flag}`

## Dica
Aponte o proxy para 127.0.0.1/localhost e portas não públicas.
