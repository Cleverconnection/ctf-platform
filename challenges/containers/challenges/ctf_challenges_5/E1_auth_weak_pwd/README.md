# Sessão Reutilizável

**Categoria:** Web

## Cenário
Uma aplicação legada continua em produção para dar suporte a funcionalidades internas críticas. O portal de administração é usado para emitir tokens de sessão que habilitam processos automatizados e integrações entre sistemas, mas credenciais padrão e senhas triviais ainda estão válidas. O mecanismo de emissão também não valida entradas nem bloqueia tentativas falhas.

## Recursos
- URL de acesso individual fornecida ao iniciar a instância do desafio.

## Objetivo
Encontrar credenciais válidas explorando senhas fracas, recuperar o token interno e utilizá-lo para acessar recursos protegidos e obter a flag.

## Flag
`ITAU2025{weak_passwords_ruin_security}`

## Dica
O token de login não é a flag; utilize-o no endpoint indicado pela aplicação para avançar.
