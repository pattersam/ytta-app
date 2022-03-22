# YTTA App Backend

*REST API of the YouTube Tag Analyser App*

## Installation

```bash
pip install -r requirements.txt
pip install -r dev_requirements.txt
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
