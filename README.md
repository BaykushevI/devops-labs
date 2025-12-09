🧰 DevOps Labs – Raspberry Pi Learning Environment

A complete, hands-on DevOps learning journey built on Raspberry Pi 5.

This repository documents a full DevOps roadmap executed on real hardware.
Every phase builds on the previous one, gradually evolving into a production-like DevOps ecosystem with automation, microservices, CI/CD pipelines, observability, and Kubernetes.

All labs are implemented on ARM64 Raspberry Pi 5, ensuring the environment is realistic, constrained, and cloud-native.

📁 Repository Structure
devops-labs/
│
├── phase-1-linux/
│   ├── lab1-basic-bash/         # System monitoring script (CPU/RAM logging)
│   └── lab2-git-workflow/       # Branching, SSH auth, feature workflow
│
├── phase-2-docker/
│   └── lab4-flask-postgres/     # Multi-service Python app (Users + Tasks + Postgres)
│       ├── users-api/           # Flask microservice + metrics + load testing
│       ├── tasks-api/           # Second Flask microservice + metrics + load testing
│       ├── database/            # Postgres 16 Alpine
│       └── docker-compose.yml   # Full multi-container architecture
│
├── phase-5-monitoring/
│   ├── prometheus.yml
│   ├── loki-config.yml
│   ├── promtail-config.yml
│   ├── dashboards/
│   │   ├── raspberry-pi-system.json
│   │   ├── docker-containers.json
│   │   └── microservices-observability.json
│   └── docker-compose.yml       # Prometheus + Grafana + Loki stack
│
├── phase-3-kubernetes/          # (K3s cluster – coming next)
├── phase-4-terraform/           # (Infrastructure as Code – coming next)
└── phase-6-ci-cd/               # (GitHub Actions CI/CD – upcoming)

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
CI/CD pipelines (upcoming)
Kubernetes (K3s) deployment (upcoming)
Infrastructure as Code (Terraform) (upcoming)
Each phase is a real DevOps scenario you would encounter in production teams.

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
Committing and merging
SSH key authentication
Renaming branches
Cleaning stale refs

✔ Lab 4 – Docker Multi-Service Architecture

Path: phase-2-docker/lab4-flask-postgres/
A realistic microservices platform including:

🟦 Users API (Flask)

Create/list users
/health, /version, /metrics, /load

🟪 Tasks API (Flask)

CRUD for tasks
Linked to Users API via shared database
Metrics + load generator

🟩 Postgres 16 (Alpine)

Shared relational database

🟧 Adminer (8084)

Browser database UI

🟡 Docker Compose

Service networking
Named containers
Persistent volumes
ARM64 image builds
This lab introduces containerization, networking, metrics, and microservice architecture.

✔ Lab 5 – Monitoring & Observability Stack

Path: phase-5-monitoring/
A complete production-style observability setup running entirely on Raspberry Pi.

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
Searchable by container, label, text
Fully integrated with Grafana Explore

✓ End Result

Full visibility into system, containers, and microservices — CPU, RAM, request rates, health, and logs — in a production-like stack.

🔮 Upcoming Labs
Phase 6 – CI/CD Pipelines (GitHub Actions)

Build ARM64 Docker images
Push to GHCR / Docker Hub
Automated deploy pipeline for Raspberry Pi
Secrets management
Deployment strategies

Phase 3 – Kubernetes (K3s)

Deploy Users & Tasks APIs to K3s
Services, Deployments, Ingress
Liveness/Readiness probes
Helm charts
Rolling updates & rollback strategies

Phase 4 – Terraform (Infrastructure as Code)

Automate provisioning
Manage Raspberry Pi config via IaC
Hybrid cloud integrations

🧠 Why Raspberry Pi?

Using real ARM64 hardware gives:
True Linux environment
Resource constraints similar to cloud micro VMs
No simulation — every mistake is real
Direct exposure to OS-level concepts (mounts, systemd, boot configs)
Excellent for Docker & K3s clusters
This project is designed as a true DevOps sandbox for learning, experimenting, and building a production-like environment step by step.

📌 Repository Status

🚧 Actively in development
🚀 New labs are added continuously
📈 Everything builds toward a full DevOps portfolio

✔ End of README

Let’s continue the journey. Next stop: CI/CD pipelines.
