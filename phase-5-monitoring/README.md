📡 Lab 5 – Monitoring & Observability Stack

Prometheus • Grafana • Loki • Promtail • cAdvisor • Node Exporter

This lab extends the DevOps learning environment on Raspberry Pi by adding a full observability stack, including metrics, logs, dashboards, and container monitoring.
The goal is to simulate a production-like monitoring setup for microservices deployed on Docker.

🚀 What We Built in Lab 5
✔ Prometheus — Metrics collection

Prometheus scrapes:

Raspberry Pi system metrics via node-exporter

Docker container metrics via cAdvisor

Microservice metrics from the Flask apps (users-api & tasks-api)

/metrics implemented using prometheus_client

Prometheus runs on port 9090.

✔ Grafana — Visualization Layer

Grafana consumes Prometheus & Loki as data sources and includes three dashboards:

Raspberry Pi System Dashboard

CPU, RAM, Temperature, Disk IO

Network traffic

Docker Containers Dashboard

CPU per container

Memory per container

Running containers overview

Microservices Dashboard

API Request Counters

Latency distributions

Logs per service (via Loki)

Grafana runs on port 3000.

✔ Loki + Promtail — Centralized Logging

Promtail collects Docker container logs from:
/var/lib/docker/containers/*/*.log

Loki stores logs and exposes them to Grafana’s "Explore" tab.

This enables:

Real-time debugging

Filtering by container, service, label

Correlating logs ↔ metrics

Loki runs on 3100.

✔ cAdvisor — Container-level metrics

Provides per-container resource usage.
Exposed at :8080.
Scraped by Prometheus via /metrics.

🧩 Architecture Overview
         ┌───────────────────────────────┐
         │         Grafana               │
         │ Dashboards & Log Explorer     │
         └───────────────▲──────────────┘
                         │
              Prometheus │   Loki
                  (metrics)   (logs)
                         │
 ┌───────────────┬───────────────┬───────────────┐
 │ Node Exporter  │   cAdvisor    │  Promtail     │
 │ (system stats) │ (containers)  │ (docker logs) │
 └───────────────┴───────────────┴───────────────┘
                         │
               Raspberry Pi (Docker)
         Users API • Tasks API • Postgres

🛠 Docker Compose Structure

All monitoring components are defined in:

phase-5-monitoring/docker-compose.yml


Services included:

lab5-node-exporter

lab5-cadvisor

lab5-prometheus

lab5-grafana

lab5-loki

lab5-promtail

📊 Dashboards

The lab includes ready JSON dashboards for import into Grafana:

dashboards/
  ├── raspberry-pi-system.json
  ├── docker-containers.json
  └── microservices-observability.json


Each dashboard shows real metrics and logs from the running apps.

🧪 How to Run Lab 5
cd phase-5-monitoring
docker compose up -d


Then open:

Grafana → http://localhost:3000

Prometheus → http://localhost:9090

cAdvisor → http://localhost:8080

Loki logs via Grafana Explore

🎯 Lab Outcome

By completing this lab, we achieved:

✔ Full observability stack
✔ Metrics for Pi, Docker, and microservices
✔ Centralized logging with Loki
✔ Real dashboards built like in production
✔ Monitoring foundation for CI/CD & Kubernetes labs

This is now a production-style monitoring setup running fully on Raspberry Pi.

✅ Next Steps (Phase 6 & Beyond)

CI/CD pipeline for microservices (GitHub Actions)

Push Docker images automatically

Deploy to Raspberry Pi via SSH or runner

Transition to Kubernetes (K3s)

Observability inside K8s using the same stack

✔ Lab 5 successfully completed.
