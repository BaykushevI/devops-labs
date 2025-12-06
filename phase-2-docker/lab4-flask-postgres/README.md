# Lab 4 – Python Microservices (Users & Tasks) with Postgres, Metrics and Load

This lab demonstrates a small microservices setup running on Docker:

- **Postgres** – shared database
- **Users API (Flask)** – manages users
- **Tasks API (Flask)** – manages tasks linked to users
- **Adminer** – web UI for Postgres
- **Metrics & Load** – basic observability endpoints

## Services & Ports

- Users API: `http://<pi-ip>:8081`
- Tasks API: `http://<pi-ip>:8082`
- Adminer: `http://<pi-ip>:8084`
- Postgres: port `5432` on the host

## Users API endpoints

- `GET /health`
- `GET /version`
- `GET /users`
- `POST /users`
- `GET /metrics`
- `GET /load?seconds=5`

## Tasks API endpoints

- `GET /health`
- `GET /version`
- `GET /tasks`
- `POST /tasks`
- `PATCH /tasks/<id>`
- `DELETE /tasks/<id>`
- `GET /metrics`
- `GET /load?seconds=5`

## How to run

From this directory:

```bash
docker compose up -d --build

