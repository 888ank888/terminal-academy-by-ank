#!/bin/bash
set -e

# Fetch subscription tier (defaults to starter)
TIER="${1:-starter}"

if [ "$TIER" = "pro" ] || [ "$TIER" = "devops_professional" ]; then
  export SANDBOX_CPU_LIMIT="0.50"
  export SANDBOX_MEM_LIMIT="1024M"
  echo "[PROVISIONER] Initializing DevOps Pro Tier (CPU Limit: ${SANDBOX_CPU_LIMIT}, RAM Limit: ${SANDBOX_MEM_LIMIT})..."
else
  export SANDBOX_CPU_LIMIT="0.25"
  export SANDBOX_MEM_LIMIT="512M"
  echo "[PROVISIONER] Initializing Socratic Starter Tier (CPU Limit: ${SANDBOX_CPU_LIMIT}, RAM Limit: ${SANDBOX_MEM_LIMIT})..."
fi

# Run docker compose using the dynamically set hardware parameters
docker compose up -d sandbox
