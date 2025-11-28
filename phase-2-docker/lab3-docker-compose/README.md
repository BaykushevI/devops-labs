# Lab 3 – Docker Compose (Postgres + Adminer)

## Goal

Learn how to run multi-container applications using Docker Compose on Raspberry Pi.

This lab creates:

- **Postgres 16** database
- **Adminer** web UI for managing the DB
- Persistent storage using Docker volumes
- Isolated container network

## Commands

### Start the stack
docker compose up -d

Stop it
docker compose down

Check running containers
docker ps

Access Adminer
http://<raspberry-pi-ip>:8084

This lab mirrors real production patterns and is a foundation for future DevOps topics:
- migrations
- app + db deployments
- environment configuration
- networking

secrets