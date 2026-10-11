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

# TP07: CI/CD con GitHub Actions

![CI/CD Pipeline](https://github.com/VAguergaray/devops-TP06/actions/workflows/cicd.yml/badge.svg)

App de notas con pipeline CI/CD completo usando GitHub Actions.

## Pipeline

| Stage | Trigger | Que hace |
|---|---|---|
| lint | push (main, develop, feature/**) y PR | flake8 en Python, yamllint en YAML |
| test | despues de lint | pytest con reporte de cobertura |
| build-push | push a main y develop | docker buildx, push a Docker Hub |
| deploy | solo push a main | SSH al servidor, compose pull + up |

## 5 Secrets requeridos

- DOCKERHUB_USERNAME
- DOCKERHUB_TOKEN
- DEPLOY_HOST
- DEPLOY_USER
- DEPLOY_SSH_KEY

## Correr tests localmente

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v --cov=. --cov-report=term-missing
```

## Flujo por rama

```text
feature/* -> lint -> test
develop   -> lint -> test -> build -> push
main      -> lint -> test -> build -> push -> deploy
```
