# Internationalização (i18n)

Este diretório armazena os arquivos de tradução baseados em gettext.

## Dependências

Instale o pacote `Babel` (ou utilize o ambiente virtual do projeto):

```bash
pip install babel
```

## Fluxo recomendado

1. **Extrair mensagens** do código-fonte para o template `messages.pot`:
   ```bash
   pybabel extract -F i18n/babel.cfg -o i18n/messages.pot .
   ```
2. **Inicializar** um novo idioma (somente na primeira vez):
   ```bash
   pybabel init -i i18n/messages.pot -d i18n -l pt_BR
   ```
3. **Atualizar** catálogos existentes após mudanças nas strings:
   ```bash
   pybabel update -i i18n/messages.pot -d i18n
   ```
4. Após tradução e revisão, **compilar** os arquivos `.po` para `.mo`:
   ```bash
   pybabel compile -d i18n
   ```

> **Nota:** Não faça commits dos arquivos compilados `.mo` antes da revisão humana.
