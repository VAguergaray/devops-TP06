# Docker Compose App de Notas

DevOps utilizando Docker Compose, Flask, PostgreSQL y Nginx.

---

# Descripción del proyecto

La aplicación consiste en una app de notas dividida en tres servicios:

- Frontend → Nginx
- Backend → Flask API
- Base de Datos → PostgreSQL

Todo el stack se administra mediante Docker Compose.

---

# Tecnologías utilizadas

- Docker
- Docker Compose
- Python 3.12
- Flask
- PostgreSQL
- Nginx
- Gunicorn

---

# Estructura del proyecto

```text
devops-TP06/
├── docker-compose.yml
├── docker-compose.override.yml
├── .env.example
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── entrypoint.sh
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── index.html
└── scripts/
    └── healthcheck.sh
