# Lab 1 – Custom NGINX Docker Image (Raspberry Pi)

## Goal

- Practice building a custom Docker image on Raspberry Pi 5
- Understand how Dockerfile instructions work (`FROM`, `COPY`)
- Run a containerized web server with a custom index page

## What this lab does

- Uses the official `nginx:alpine` image as a lightweight base
- Replaces the default `/usr/share/nginx/html/index.html` with a custom `index.html`
- Exposes the container on port `8081` mapped to container port `80`

## How to build

From this directory:

docker build -t mynginx-custom:1.0 .

How to run

docker run -d -p 8081:80 --name customnginx mynginx-custom:1.0

Then open in a browser:

http://<raspberry-pi-ip>:8081

How to stop and remove
docker stop customnginx
docker rm customnginx