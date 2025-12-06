# Lab 4 – Python Flask + Postgres + Docker Compose

## Endpoints

- `GET /health` – app + DB health
- `GET /version` – shows `APP_VERSION` and `GIT_COMMIT`
- `GET /users` – list users
- `POST /users` – create user `{ "name": "...", "email": "..." }`

## How to run

From this directory:

```bash
docker compose up -d --build
