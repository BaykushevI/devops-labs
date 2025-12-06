DevOps Labs – Raspberry Pi Learning Environment

A fully hands-on DevOps learning journey executed on Raspberry Pi 5.
The goal: develop real, production-like DevOps experience by building automation, microservices, CI/CD pipelines, containerized apps, monitoring systems, and Kubernetes clusters — all running on actual ARM hardware.

This repository evolves step-by-step into a full DevOps portfolio.

🚀 Repository Structure
devops-labs/
├── phase-1-linux/
│   └── labs/
│       ├── lab1-basic-bash/
│       └── lab2-git-workflow/
│
├── phase-2-docker/
│   └── lab4-flask-postgres/   ← Multi-service Python app (Users + Tasks + Postgres)
│       ├── users-api
│       ├── tasks-api
│       ├── database (Postgres)
│       └── metrics + load testing endpoints
│
├── phase-3-kubernetes/        (K3s cluster – coming soon)
├── phase-4-terraform/         (Infrastructure as Code – coming soon)
└── phase-5-monitoring/        (Prometheus + Grafana + Loki – coming soon)

🎯 Project Purpose

This repository acts as a DevOps sandbox, built to simulate real-world scenarios:

✔ Linux administration (filesystems, boot configuration, services)
✔ Bash scripting & automation
✔ Git workflow (branches, PRs, feature isolation)
✔ Docker & multi-container environments
✔ Microservices architecture on ARM
✔ CI/CD using GitHub Actions
✔ Kubernetes (K3s on Raspberry Pi)
✔ Infrastructure as Code (Terraform)
✔ Monitoring & Observability (Prometheus, Grafana, Loki)
✔ Logging, metrics, health checks, service load testing

Everything here is built as if preparing for a DevOps Engineer role, with real workflows, real projects, real tools.

🧪 Completed Labs
### ✔ Lab 1 – Basic Bash System Monitor

Path: phase-1-linux/labs/lab1-basic-bash/
A Bash script that logs CPU and RAM usage with timestamps.
Covers: cron-like scheduling, Linux metrics, logging formats, shell scripting.

✔ Lab 2 – Git Workflow Foundations

Path: phase-1-linux/labs/lab2-git-workflow/
Feature branches, commits, merging, branch cleanup, SSH authentication.

✔ Lab 4 – Docker Multi-Service Application (Python + Postgres)

Path: phase-2-docker/lab4-flask-postgres/

A production-like microservices setup:

🟦 Users API (Flask)

Create/list users

Health check

Version endpoint

Metrics endpoint (uptime, CPU, RAM, total users)

Load generator for stress testing

🟪 Tasks API (Flask)

Create / update / delete tasks

Linked to users via foreign key

Health, version, metrics, load endpoints

🟩 Postgres Database (16 Alpine)

Shared DB for both APIs

🟧 Adminer

In-browser DB GUI at port 8084

🟡 Docker Compose Orchestration
All services run together with isolated containers and shared networks.

This lab demonstrates:

containerization

service discovery

DB migrations

metrics + observability

handling load

building & running ARM64 images

🔮 Upcoming Labs (already planned)
Phase 2 – Docker (continuation)

Docker networking & volumes

Container health checks

CI build automation

Secure Dockerfiles

Phase 3 – Kubernetes (K3s on Raspberry Pi)

Deploy microservices to a real cluster

Services, Deployments, Ingress

Helm charts

Secrets & ConfigMaps

Rolling updates

Phase 4 – Terraform

Automating infrastructure provisioning

Raspberry Pi + cloud hybrid deployment

Phase 5 – Monitoring & Logging

Prometheus node + exporters

Grafana dashboards

Loki log aggregation

Alertmanager rules

🧠 Why Raspberry Pi?

Real ARM Linux environment

Forces you to work like in cloud-native teams (ARM is used at scale)

No “simulated DevOps” — everything is real

Great platform for Kubernetes, Docker, networking labs

This repo serves as a true DevOps playground designed to grow into a full, production-like ecosystem.

📌 Status

This repository is actively developed.
New labs and upgrades are added as the learning roadmap progresses.

Follow commits & branches for continuous evolution.
