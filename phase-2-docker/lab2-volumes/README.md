# Lab 2 – Docker Volumes and Bind Mounts

## Goals

- Understand the difference between Docker **volumes** and **bind mounts**
- Persist NGINX web content across container recreation
- Edit files on the host and serve them directly from a container

---

## Part 1 – Named Volume (`nginx_html`)

### Create the volume

docker volume create nginx_html
Run NGINX with the volume

docker run -d \
  --name nginx-vol \
  -p 8082:80 \
  -v nginx_html:/usr/share/nginx/html \
  nginx:alpine

Add content to the volume

docker exec -it nginx-vol sh
cd /usr/share/nginx/html
echo "<h1>Served from Docker volume on Raspberry Pi</h1>" > index.html
exit
Open in a browser:

http://<raspberry-pi-ip>:8082
Stop and remove the container:

docker stop nginx-vol
docker rm nginx-vol
Run a new container using the same volume:

docker run -d \
  --name nginx-vol2 \
  -p 8082:80 \
  -v nginx_html:/usr/share/nginx/html \
  nginx:alpine
The page is still there → data lives in the volume, not the container.

Part 2 – Bind Mount
From the directory phase-2-docker/lab2-volumes, create:

mkdir -p html
nano html/index.html
Then run:

docker run -d \
  --name nginx-bind \
  -p 8083:80 \
  -v "$(pwd)/html:/usr/share/nginx/html:ro" \
  nginx:alpine

Open:

http://<raspberry-pi-ip>:8083
Any changes to html/index.html on the host are reflected immediately in the browser.

This lab demonstrates how to manage persistent data and host-edited content in Docker, which is essential for real-world DevOps workflows.
