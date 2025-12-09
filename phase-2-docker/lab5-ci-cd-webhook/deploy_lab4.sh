#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="/home/ibayk/devops-labs/phase-2-docker/lab5-ci-cd-webhook/deploy.log"

check_service() {
    name=$1
    port=$2

    echo "[Deploy] Checking ${name} on port ${port}..."

    for i in {1..15}; do
        status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:${port}/health || echo "000")

        if [ "$status" == "200" ]; then
            echo "${name}: OK"
            return 0
        fi

        sleep 2
    done

    echo "${name}: FAIL (last status: ${status})"
    return 1
}

{
  echo "========== $(date '+%Y-%m-%d %H:%M:%S') – Starting Lab4 deploy =========="

  cd /home/ibayk/devops-labs/phase-2-docker/lab4-flask-postgres

  echo "[Deploy] Pulling latest images from GHCR..."
  docker compose pull

  echo "[Deploy] Restarting Lab4 stack..."
  docker compose down
  docker compose up -d

  echo "[Deploy] Waiting for containers to start..."

  users_status=1
  tasks_status=1

  check_service "users-api" 8081 && users_status=0
  check_service "tasks-api" 8082 && tasks_status=0

  if [ $users_status -ne 0 ] || [ $tasks_status -ne 0 ]; then
      echo "[Deploy] One or more services failed health check."
      echo "[Deploy] DONE with ERRORS."
      exit 1
  fi

  echo "[Deploy] All services are healthy."
  echo "[Deploy] DONE successfully."
} >> "$LOG_FILE" 2>&1

