🧰 DevOps Labs – Raspberry Pi Learning Environment

A complete, hands-on DevOps learning journey built on Raspberry Pi 5.

This repository documents a full DevOps roadmap executed on real hardware. Every phase builds on the previous one, gradually evolving into a production-like DevOps ecosystem with automation, microservices, CI/CD pipelines, observability, and Kubernetes.

All labs are implemented on ARM64 Raspberry Pi 5, ensuring the environment is realistic, constrained, and cloud-native.

📁 Repository Structure
devops-labs/
│
├── phase-1-linux/
│   ├── lab1-basic-bash/              # System monitoring script (CPU/RAM logging)
│   └── lab2-git-workflow/            # Branching, SSH auth, feature workflow
│
├── phase-2-docker/
│   └── lab4-flask-postgres/          # Multi-service Python app (Users + Tasks + Postgres)
│       ├── users-api/                # Flask microservice + metrics + load testing
│       ├── tasks-api/                # Second microservice + metrics + load testing
│       ├── database/                 # Postgres 16 Alpine
│       └── docker-compose.yml        # Full multi-container architecture
│
├── phase-5-monitoring/
│   ├── prometheus.yml
│   ├── loki-config.yml
│   ├── promtail-config.yml
│   ├── dashboards/
│   │   ├── raspberry-pi-system.json
│   │   ├── docker-containers.json
│   │   └── microservices-observability.json
│   └── docker-compose.yml            # Prometheus + Grafana + Loki stack
│
├── phase-5-ci-cd/                    # (New) Webhook-based automated deployment
│   ├── webhook_server.py             # FastAPI webhook receiver
│   ├── deploy_lab4.sh                # Automated pull + restart + health checks
│   └── systemd service file          # webhook.service (for auto-start)
│
├── phase-3-kubernetes/               # (K3s cluster – coming next)
├── phase-4-terraform/                # (Infrastructure as Code – coming next)
└── phase-6-ci-cd/                    # (Full GitHub Actions pipelines – upcoming)

🎯 Project Purpose

This repository simulates real DevOps challenges, workflows, and infrastructure by implementing:

Linux administration (system services, permissions, boot config)

Bash scripting & automation

Git branching, merges & SSH authentication

Docker containers and multi-service orchestration

Microservices architecture on ARM hardware

Monitoring & Logging with Prometheus, Grafana, Loki

Metrics instrumentation with Prometheus client libraries

Load testing and performance troubleshooting

CI/CD pipeline (GitHub Actions → GHCR → Webhook Deployments)

Kubernetes (K3s) deployment (upcoming)

Infrastructure as Code (Terraform) (upcoming)

Each phase represents a real DevOps scenario common in modern engineering teams.

✅ Completed Labs
✔ Lab 1 – Basic Bash System Monitor

Path: phase-1-linux/labs/lab1-basic-bash/

A Bash script that logs CPU and RAM usage with timestamps.

Topics covered:

Linux filesystem basics

Shell scripting

Logging formats

Cron-style looping

Timestamps & output redirection

✔ Lab 2 – Git Workflow Foundations

Path: phase-1-linux/labs/lab2-git-workflow/

Hands-on Git workflow simulation:

Creating feature branches

Commit & merge workflow

SSH key authentication

Renaming branches

Cleaning stale refs

✔ Lab 4 – Docker Multi-Service Architecture

Path: phase-2-docker/lab4-flask-postgres/

A realistic microservices platform including:

🟦 Users API (Flask)

Create/list users

/health, /version, /metrics, /load endpoints

🟪 Tasks API (Flask)

CRUD for tasks

Linked to Users API via Postgres

/health, /metrics, /load

🟩 Postgres 16 (Alpine)

Shared relational DB.

🟧 Adminer (port 8084)

Browser-based DB UI.

🟡 Docker Compose

Named containers

Service network

ARM64 image builds

Persistent volumes

This lab introduces containerization, networking, metrics, and microservice architecture.

✔ Lab 5 – Monitoring & Observability Stack

Path: phase-5-monitoring/

A complete production-style observability setup running entirely on Raspberry Pi:

✓ Prometheus

Scrapes metrics from:

Raspberry Pi system (node_exporter)

Docker containers (cAdvisor)

Users API & Tasks API (/metrics)

✓ Grafana

Dashboards implemented:

Raspberry Pi System Dashboard

Docker Containers Dashboard

Microservices Observability Dashboard (metrics + logs)

✓ Loki + Promtail

Centralized log aggregation:

Real-time logs from all Docker containers

Searchable by container, label, or text

Integrated with Grafana Explore

End Result:
Full visibility across system, containers, and microservices.

✔ Lab 5B – Continuous Deployment Webhook (Raspberry Pi)

Path: phase-5-ci-cd/

A lightweight CD system triggered by GitHub tag pushes:

✓ FastAPI Webhook Server

Listens for GitHub Webhook events:

POST /deploy

✓ Deployment Script (deploy_lab4.sh)

Automates:

Pull new images from GHCR

Restart entire microservices stack

Perform health checks on:

http://localhost:8081/health (users-api)

http://localhost:8082/health (tasks-api)

✓ Systemd Service

Ensures the webhook server is always running on boot.

✓ Integration with GitHub Actions

Tagging a release (v0.0.x) triggers:

Multi-arch Docker image build

Push to GitHub Container Registry

Raspberry Pi auto-deployment via webhook

This completes the first half of the CI/CD pipeline.

🔮 Upcoming Labs
Phase 6 – Full CI/CD Pipelines (GitHub Actions)

Build ARM64 Docker images

Push to GHCR / Docker Hub

Automated Raspberry Pi deployments

Secrets management

Deployment strategies

Phase 3 – Kubernetes (K3s)

Deploy Users & Tasks APIs to K3s

Services, Deployments, Ingress

Liveness/Readiness probes

Helm charts

Rolling updates & rollbacks

Phase 4 – Terraform (IaC)

Automate provisioning

Raspberry Pi configuration via code

Hybrid cloud integrations

🧠 Why Raspberry Pi?

Using real ARM64 hardware provides:

True Linux environment

Resource constraints similar to cloud micro-VMs

No simulation — every mistake is real

Direct exposure to OS-level concepts (mounts, boot, systemd)

Excellent platform for Docker & K3s clusters

This repository acts as a true DevOps sandbox for learning, experimenting, and building a production-like environment.

📌 Repository Status

🚧 Actively in development
🏗️ New labs added continuously
📈 Everything builds toward a complete DevOps portfolio

✔ End of README

Let’s continue the journey — next stop: Full CI/CD automation.
