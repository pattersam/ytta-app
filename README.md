# YTTA App

YouTube Tag Analyser App

## Installation

```bash
pip install -r requirements.txt
```

## Building / running as a container

### Build

```bash
docker build -t app .
```

### Run

```bash
docker run -p 8000:8000 app
```

### List all containers

```bash
docker ps -a
```

### Remove all containers

```bash
docker rm -f $(docker ps -a -q)
```
