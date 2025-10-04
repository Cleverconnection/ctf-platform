docker exec -it itau-chall-manager-1 bash -lc '\
  SCENARIO_NAME=web-102 ACTION=create \
  TEMPLATE_VMID=2203 CLONE_MODE=full \
  VMID_RANGE_START=2200 VMID_RANGE_END=2300 \
  /scenarios/_runner/exec-scenario.sh'
