#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"
LOGFILE="$ROOT_DIR/bulk_sync.log"
TOKEN_ENV="${CTFD_TOKEN:-}"

echo "Starting bulk sync at $(date)" | tee "$LOGFILE"

# 1) find all challenge.yml
echo "Scanning for challenge.yml..." | tee -a "$LOGFILE"
mapfile -t YAMLS < <(find . -type f -name 'challenge.yml' -print)

if [ ${#YAMLS[@]} -eq 0 ]; then
  echo "No challenge.yml found. Exiting." | tee -a "$LOGFILE"
  exit 1
fi

echo "Found ${#YAMLS[@]} challenge.yml files." | tee -a "$LOGFILE"

# 2) register each directory in .ctf/config
echo "Adding challenge directories to .ctf/config..." | tee -a "$LOGFILE"
for y in "${YAMLS[@]}"; do
  dir=$(dirname "$y")
  echo "[add] $dir" | tee -a "$LOGFILE"
  ctf challenge add "$dir" || true
done

# 3) lint and verify all
echo "Running ctf challenge lint..." | tee -a "$LOGFILE"
ctf challenge lint 2>&1 | tee -a "$LOGFILE"

echo "Running ctf challenge verify..." | tee -a "$LOGFILE"
ctf challenge verify 2>&1 | tee -a "$LOGFILE"

# 4) Install all challenges as hidden (safe) — change if you want visible
echo "Installing all challenges (hidden)..." | tee -a "$LOGFILE"
ctf challenge install --hidden 2>&1 | tee -a "$LOGFILE"

# 5) Sync to make sure local state and remote state aligned
echo "Running ctf challenge sync..." | tee -a "$LOGFILE"
ctf challenge sync 2>&1 | tee -a "$LOGFILE"

echo "Bulk sync finished at $(date)" | tee -a "$LOGFILE"
