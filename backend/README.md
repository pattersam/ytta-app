# YTTA App Backend

*REST API of the YouTube Tag Analyser App*

## Installation

```bash
pip install -r requirements.txt
pip install -r dev_requirements.txt
```

## Celery

### Start a worker

```bash
celery -A app.worker worker -l info -Q ytta-celery
```

## Alembic migrations

### Update to latest version

```bash
alembic upgrade head
```

### Make a new version

```bash
alembic revision --autogenerate -m "..."
```

## Building / running as a container

### Build

```bash
docker build -t backend .
```

### Run

```bash
docker run -p 8000:8000 backend
```

### List all containers

```bash
docker ps -a
```

### Remove all containers

```bash
docker rm -f $(docker ps -a -q)
```
