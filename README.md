# ctf_clever
Plataforma de CTF Fork do CTFD e do Chall-manager

## Atualização de traduções

Para extrair e atualizar as mensagens de tradução do projeto execute:

```bash
pybabel extract -F i18n/babel.cfg -o i18n/messages.pot .
pybabel update -l pt_BR -i i18n/messages.pot -d i18n
```

Revise o diff gerado (`git diff`) e submeta as alterações resultantes.
