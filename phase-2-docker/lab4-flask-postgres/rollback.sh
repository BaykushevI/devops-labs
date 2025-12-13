#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: ./rollback.sh <tag>"
  echo "Example: ./rollback.sh v0.1.3"
  exit 1
fi

TAG="$1"
export APP_TAG="$TAG"

echo "[rollback] Rolling back to tag: $APP_TAG"
docker compose pull
docker compose up -d
docker ps

echo "[rollback] Smoke tests..."
curl -fsS http://localhost:8081/health >/dev/null
curl -fsS http://localhost:8082/health >/dev/null
echo "[rollback] OK"
