# Itaú CTF – Pacote de Desafios (E1–E20)

Este diretório reúne vinte desafios independentes em Flask pensados para a edição 2025 do CTF Itaú. Cada serviço possui front-end padronizado com a identidade visual solicitada e um Dockerfile dedicado para facilitar o build e a publicação em ambientes CTFd, Proxmox ou infraestrutura similar.

## Visão geral dos desafios

| Desafio | Tema | Enredo | Flag padrão |
|---------|------|--------|-------------|
| `E1_auth_weak_pwd` | Autenticação | Portal legado usa senhas triviais para gerar tokens internos. | `ITAU2025{weak_passwords_ruin_security}` |
| `E2_jwt_noexp` | API JWT | Token sem expiração permite manipular o payload para escalar privilégios. | `ITAU2025{jwt_without_expiration}` |
| `E3_idor_account` | IDOR | Consulta de contas não verifica o proprietário e expõe dados executivos. | `ITAU2025{idor_bank_accounts}` |
| `E4_open_redirect` | SSRF | Proxy de integrações faz fetch de qualquer URL informada pelo operador. | `ITAU2025{ssrf_proxy_to_flag}` |
| `E5_file_read` | Path traversal | Leitor corporativo acessa caminhos arbitrários dentro do container. | `ITAU2025{path_traversal_master}` |
| `E6_sql_injection_basic` | SQL Injection | Relatório comercial monta consultas com concatenação simples permitindo UNION. | `ITAU2025{sqli_in_the_branch}` |
| `E7_xxe_simple` | XXE | Importador XML aceita entidades externas e revela códigos internos. | `ITAU2025{xxe_into_core}` |
| `E8_upload_exec_hint` | Upload inseguro | Central de uploads publica arquivos com nomes previsíveis ao lado de notas sigilosas. | `ITAU2025{predictable_upload_leak}` |
| `E9_cors_wildcard` | CORS | API responde com `Access-Control-Allow-Origin: *`, expondo o token de sessão. | `ITAU2025{cors_wildcard_token}` |
| `E10_exposed_swagger` | Swagger público | Documentação interna vazou com exemplos contendo chaves reais. | `ITAU2025{swagger_spill}` |
| `E11_info_headers` | Headers verbosos | Healthcheck entrega cabeçalhos com caminhos e dicas de arquivos sensíveis. | `ITAU2025{headers_tell_secrets}` |
| `E12_query_creds` | Credenciais na URL | Link de backup inclui token em query string compartilhado por e-mail. | `ITAU2025{creds_in_query}` |
| `E13_log_injection` | Log injection | Painel de incidentes grava input bruto permitindo forjar entradas válidas. | `ITAU2025{logs_are_trust_issue}` |
| `E14_timestamp_replay` | Replay de transações | Motor antifraude aceita o mesmo timestamp diversas vezes e acumula créditos. | `ITAU2025{timestamp_replay_attack}` |
| `E15_weak_crypto` | Criptografia fraca | Tokens usam AES-ECB com chave derivada em MD5, permitindo corte e montagem. | `ITAU2025{weak_crypto_modes}` |
| `E16_public_backup` | Backup público | Arquivo `backup.zip` fica acessível na raiz com flag embutida. | `ITAU2025{public_backup_flag}` |
| `E17_password_reset_enum` | Enumeração | Portal de reset aceita qualquer ID numérico e retorna link privilegiado. | `ITAU2025{reset_enum_abuse}` |
| `E18_missing_tls_redirect` | TLS opcional | Serviço expõe cookies de sessão mesmo quando acessado via HTTP. | `ITAU2025{tls_redirect_missing}` |
| `E19_file_download_path` | Download inseguro | Endpoint de download concatena caminhos permitindo fuga do diretório. | `ITAU2025{file_download_traversal}` |
| `E20_rate_limit_none` | Brute force | Validador de OTP não impõe rate limit, permitindo força bruta ao token. | `ITAU2025{rate_limit_bypass}` |
# Itaú CTF – Pacote de Desafios (E1–E5)

Este diretório contém cinco desafios em formato de containers independentes para uso em um CTF baseado em CTFd, Proxmox ou infraestrutura similar. Cada desafio possui uma aplicação Flask com um front-end simples voltado para laboratório e o respectivo `Dockerfile` para geração da imagem.

## Visão geral dos desafios

| Desafio | Tema | Vetor explorado |
|---------|------|-----------------|
| `E1_auth_weak_pwd` | Portal de autenticação | Senhas fracas armazenadas em texto puro. |
| `E2_jwt_noexp` | API com JWT | Token sem expiração permitindo manipulação do payload. |
| `E3_idor_account` | Consulta de contas | Falta de controle de acesso nas rotas de conta (IDOR). |
| `E4_open_redirect` | Proxy SSRF | Proxy que busca URLs arbitrárias sem validação. |
| `E5_file_read` | File reader | Junção de caminhos vulnerável a path traversal. |

## Flags fixas

Cada serviço já inclui uma flag padrão pensada para o evento de 2025. Elas também são gravadas automaticamente em `/flag` durante o start do container.

| Desafio | Flag padrão |
|---------|-------------|
| `E1_auth_weak_pwd` | `ITAU2025{weak_passwords_ruin_security}` |
| `E2_jwt_noexp` | `ITAU2025{jwt_without_expiration}` |
| `E3_idor_account` | `ITAU2025{idor_bank_accounts}` |
| `E4_open_redirect` | `ITAU2025{ssrf_proxy_to_flag}` |
| `E5_file_read` | `ITAU2025{path_traversal_master}` |

## Estrutura

```
ctf_challenges_5/
  E*/
    app.py         # Aplicação Flask vulnerável
    templates/     # Front-end com identidade visual unificada
    Dockerfile     # Receita da imagem do container
```

Todos os serviços escrevem a flag padrão em `/flag` durante a inicialização, permitindo integração com checagens automatizadas. As flags podem ser sobrescritas via variável de ambiente `FLAG` no `docker run` se necessário.

## Como construir

Cada desafio pode ser construído individualmente:

```bash
cd ctf_challenges_5/E6_sql_injection_basic
sudo docker build -t ctf/e6_sql_injection_basic:latest .
```

Altere o diretório/tag conforme o desafio desejado (`E1` até `E20`).
    templates/     # Front-end amigável para o desafio
    Dockerfile     # Receita da imagem do container
```

## Como construir

Cada desafio pode ser construído de forma independente:

```bash
cd ctf_challenges_5/E1_auth_weak_pwd
sudo docker build -t ctf/e1_auth_weak_pwd:latest .
```

Altere o diretório e a tag conforme o desafio desejado (`E2`, `E3`, etc.).

## Como executar localmente

```bash
sudo docker run -it --rm \
  -p 15006:8080 \
  ctf/e6_sql_injection_basic:latest
```

Defina `FLAG="ITAU2025{custom}"` durante o `docker run` se quiser personalizar uma instância específica.

## Observações

- Nenhum desafio implementa controles de segurança reais; use apenas em ambientes isolados.
- Os front-ends seguem o layout escuro solicitado e oferecem dicas narrativas para orientar os participantes.
- Recursos auxiliares (arquivos, bancos, logs) são criados automaticamente dentro do container na primeira execução.
  -e FLAG="CTF{FLAG_REAL}" \
  -p 15001:8080 \
  ctf/e1_auth_weak_pwd:latest
```

Se desejar alterar a flag para uma instância específica, defina a variável de ambiente `FLAG` durante o `docker run`.
A flag também é escrita em `/flag` dentro do container, facilitando integrações com scripts de verificação.

## Observações

- Os desafios não implementam mecanismos de proteção deliberadamente.
- O front-end facilita o onboarding de participantes e pode ser customizado com identidade visual.
- Certifique-se de isolar os containers em ambientes seguros e descartar após o evento.

Bom CTF! 🏦


## Desafios Médios (20 pontos)

| Desafio | Tema | Resumo | Flag padrão |
|---------|------|--------|-------------|
| `M01_auth_bypass_logic` | Auth lógico | Fluxo MFA confia em etapa enviada pelo cliente permitindo pular o token. | `ITAU2025{auth_logic_mfa_bypass}` |
| `M02_jwt_kid_attack` | JWT | Cabeçalho `kid` e algoritmo `none` aceitos permitem forjar tokens admin. | `ITAU2025{jwt_kid_none_alg}` |
| `M03_ssrf_internal_svc` | SSRF | Proxy de integrações alcança serviços internos com cabeçalhos customizados. | `ITAU2025{ssrf_internal_service}` |
| `M04_concurrent_transfer_race` | Race | Transferências concorrentes debitam o mesmo saldo e duplicam créditos. | `ITAU2025{race_condition_transfer}` |
| `M05_payment_replay` | Replay | Pagamentos sem idempotência acumulam bônus ilimitados. | `ITAU2025{payment_replay_bonus}` |
| `M06_xml_dos_xxe_combo` | XML/XXE | Parser resolve entidades externas expondo `/flag` e aceita payloads DoS. | `ITAU2025{xml_xxe_resource_exhaust}` |
| `M07_insecure_deserialize` | Deserialização | Servidor Java deserializa objetos arbitrários permitindo ação `admin`. | `ITAU2025{java_insecure_deserialize}` |
| `M08_supply_chain_devops` | Supply chain | Pipeline expõe artefato com segredos e flag. | `ITAU2025{supply_chain_artifact}` |
| `M09_privilege_escalation_api` | API roles | Merge patch aceita string em `role` promovendo usuário a admin. | `ITAU2025{api_privilege_escalation}` |
| `M10_ssrf_s3_misuse` | SSRF/S3 | Proxy acessa bucket interno via URL arbitrária. | `ITAU2025{ssrf_s3_traversal}` |
| `M11_confd_leak` | Config leak | Endpoint `config` devolve segredos de produção sem filtro. | `ITAU2025{config_endpoint_leak}` |
| `M12_otp_bypass` | OTP | Códigos previsíveis dependem apenas dos dígitos do documento. | `ITAU2025{predictable_otp_bypass}` |
| `M13_csrf_api` | CSRF | API com cookies e CORS liberado permite transferências sem token. | `ITAU2025{csrf_cookie_api}` |
| `M14_account_merge_bug` | Merge | Fusão retorna dados completos da conta secundária com flag. | `ITAU2025{account_merge_disclosure}` |
| `M15_ssrf_internal_metadata` | SSRF | Ferramenta lê serviço de metadados interno e vaza credenciais. | `ITAU2025{metadata_ssrf_flag}` |
| `M16_race_balance_check` | Race | Saques simultâneos deixam saldo negativo liberando flag. | `ITAU2025{race_negative_balance}` |
| `M17_timing_attack` | Timing | Comparação lenta de senha revela usuário/senha por tempo. | `ITAU2025{timing_leak_username}` |
| `M18_insecure_file_serve` | Storage | Gateway concatena caminho permitindo acesso a objetos privados. | `ITAU2025{object_storage_flag}` |
| `M19_authorization_header_splitting` | Headers | Cliente define `role` via header dividido alcançando privilégios. | `ITAU2025{auth_header_split}` |
| `M20_log_forensics_tamper` | Logs | Console registra entradas sem sanitização e expõe flag em export. | `ITAU2025{log_tamper_flag}` |
