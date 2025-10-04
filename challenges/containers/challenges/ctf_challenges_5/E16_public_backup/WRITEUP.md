# Writeup — Backup Público

1. Acesse a raiz do serviço e identifique o arquivo `backup.zip` ou similar disponível para download.
2. Faça o download do arquivo utilizando `curl` ou o navegador.
3. Extraia o conteúdo com `unzip backup.zip` e explore os diretórios internos.
4. Procure por arquivos chamados `flag.txt`, `proof.txt` ou configurações contendo tokens.
5. Leia o arquivo indicado e registre a flag `ITAU2025{public_backup_flag}`.

## Lições
- Nunca deixe backups expostos em diretórios acessíveis publicamente.
- Utilize autenticação e URLs temporárias ao compartilhar arquivos sensíveis.
- Automatize rotinas de limpeza para remover artefatos de manutenção.
