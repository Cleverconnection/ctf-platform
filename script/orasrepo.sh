# Do host
REG="localhost:5000/ctf/scenarios/web-hello:v1"
cd /path/to

# Constrói uma lista Bash onde cada arquivo vira "arquivo:application/vnd.ctfer-io.file"
mapfile -t FILES < <(find my-challenge -type f -printf '%p:application/vnd.ctfer-io.file\n')

# Publica com artifact-type de "cenário"
oras push --plain-http "$REG" \
  --artifact-type application/vnd.ctfer-io.scenario \
  "${FILES[@]}"
