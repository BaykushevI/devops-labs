📘 Phase 5 – Monitoring, Logging & CI/CD Webhook Deployment
Real DevOps Engineering Journey on Raspberry Pi 5
🧩 Overview

Phase 5 represents the first “production-grade” milestone in this DevOps learning environment running on a Raspberry Pi 5.
Here, we combined three essential pillars of modern infrastructure:

Monitoring → Prometheus, Node Exporter, cAdvisor

Logging → Loki + Promtail

Automated Deployment → GitHub Actions CI + Raspberry Pi Webhook-based CD

The goal was to build a realistic observability and deployment workflow comparable to what exists in real engineering teams, but fully adapted for ARM hardware and a home-lab environment.

This phase included several real engineering challenges: registry permissions, health check failures, multi-architecture image builds, Python virtual environments, systemd services, and debugging networking issues inside Docker.

🏗️ Architecture
                   ┌──────────────────────────┐
                   │       GitHub Repo        │
                   │   devops-labs (public)   │
                   └─────────────┬────────────┘
                                 │
                         GitHub Actions CI
               (Build & Push multi-arch Docker images)
                                 │
                                 ▼
                   ┌──────────────────────────┐
                   │    GHCR Container Reg    │
                   └─────────────┬────────────┘
                                 │ Webhook Trigger
                                 ▼

┌───────────────────────────────────────────────────────────────┐
│            Raspberry Pi 5 – Production Environment             │
│                                                               │
│   ┌───────────────────┐       ┌───────────────────┐           │
│   │   Prometheus       │◀──────│   Node Exporter    │           │
│   └───────────────────┘       └───────────────────┘           │
│           ▲                                                     │
│           │ Scrapes                                             │
│           ▼                                                     │
│   ┌───────────────────┐       ┌────────────────────────┐         │
│   │    cAdvisor        │◀────▶│ Docker Container Stats │         │
│   └───────────────────┘       └────────────────────────┘         │
│                                                                   │
│   ┌────────────────────────────────────────────────────────────┐  │
│   │ Grafana Dashboards (system, containers, microservices)     │  │
│   └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│   ┌──────────────────────┐     ┌──────────────────────────────┐   │
│   │ Loki (log backend)   │◀────│ Promtail (log shipper)       │   │
│   └──────────────────────┘     └──────────────────────────────┘   │
│                                                                   │
│   ┌────────────────────────────────────────────────────────────┐  │
│   │ FastAPI Webhook Server (systemd service)                   │  │
│   │ Triggers deploy_lab4.sh on tag push events                 │  │
│   └────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘

🧪 What Was Built
✔ Prometheus – metrics collection
✔ Node Exporter – host-level monitoring
✔ cAdvisor – container-level monitoring
✔ Loki – centralized logs
✔ Promtail – log shipper
✔ Grafana dashboards

System dashboard

Docker containers dashboard

Microservices (users-api, tasks-api) dashboard

✔ GitHub Actions CI

Multi-arch Docker builds (arm64 + amd64) pushed to GHCR.

✔ Webhook-based CD on Raspberry Pi

A Python FastAPI server receives GitHub webhook events, pulls new images, redeploys the stack, and performs health checks.

🔥 Real Engineering Challenges & How They Were Solved

This section demonstrates the actual engineering effort, not just a scripted tutorial.
These real issues + fixes are exactly what DevOps reviewers appreciate.

❌ 1. GHCR Rejecting Image Uploads

Errors:

invalid reference format: must be lowercase
denied: unauthorized

🧠 Root Cause

GHCR requires that repository and image names use strict lowercase.

✔ Fix

Converted:

ghcr.io/BaykushevI/devops-labs/users-api


to:

ghcr.io/baykushevi/devops-labs/users-api

❌ 2. PAT (Personal Access Token) Missing Package Permissions

GHCR refused pushes:

denied: insufficient permissions

🧠 Root Cause

Fine-grained tokens did not expose write:packages scope.
This confused the UI flow.

✔ Fix

Created PAT (classic) with:

write:packages

read:packages

Then logged in:

echo "$TOKEN" | docker login ghcr.io -u BaykushevI --password-stdin

❌ 3. CI/CD Images Failed to Pull on the Raspberry Pi

The Pi displayed:

manifest unknown
unauthorized

🧠 Root Cause

The automated workflow initially didn’t build multi-architecture images.

✔ Fix

Updated the GitHub Actions workflow:

platforms: linux/amd64,linux/arm64


Now GHCR stores multi-arch manifests, and the Pi can pull successfully.

❌ 4. Health Checks Failing Immediately After Deployment

The webhook returned:

{"status": "failed", "users-api": "down", "tasks-api": "down"}

🧠 Root Cause

The microservices listen on port 5000, but are exposed on 8081/8082 via Docker Compose.

The health check script was checking the wrong port.

✔ Fix

Updated deploy_lab4.sh:

curl -s -o /dev/null -w "%{http_code}" http://localhost:$port/health


Once corrected → the automated health validation finally passed.

❌ 5. systemd Service Could Not Start the Webhook Server

Common error:

File not found: webhook_server.py

🧠 Root Cause

WorkingDirectory was missing, so systemd executed from /.

✔ Fix
WorkingDirectory=/home/ibayk/devops-labs/phase-2-docker/lab5-ci-cd-webhook
ExecStart=/home/.../venv/bin/uvicorn webhook_server:app --host 0.0.0.0 --port 9000


After a reload + restart, the webhook server ran flawlessly.

❌ 6. Python Package Installation Blocked by Debian PEP 668

Debian bookworm restricts system-wide pip installs.
Initial installs failed.

✔ Fix

Created a virtual environment:

python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn[standard]


Problem resolved permanently.

🚀 Final Result — Fully Working CI + CD Pipeline
CI (GitHub Actions)

On every tag push (v*):

Build Docker images for arm64 + amd64

Push to GHCR

Tag as both latest and versioned

CD (Custom Webhook on Raspberry Pi)

GitHub → Webhook → Pi triggers:

docker compose pull
docker compose down
docker compose up -d


Then:

15 retries

verifies /health on 8081 and 8082

returns JSON success or failure

Successful result:

{"status": "success", "exit_code": 0}


This is production behavior, implemented on a Raspberry Pi lab.

🏁 What This Phase Demonstrates

✔ Ability to design a real observability stack
✔ Understanding of CI/CD pipelines end-to-end
✔ Ability to debug real infrastructure issues
✔ Experience with multi-architecture container builds
✔ systemd service creation and troubleshooting
✔ Practical use of webhooks and automation scripting
✔ Strong DevOps engineering workflow reasoning

This is the first phase that truly transforms the Raspberry Pi project into a self-deploying microservices platform.
