# YTTA App

[![pipeline status](https://gitlab.com/youtube-tag-analyser/ytta-app/badges/main/pipeline.svg)](https://gitlab.com/youtube-tag-analyser/ytta-app/-/commits/main) [![coverage report](https://gitlab.com/youtube-tag-analyser/ytta-app/badges/main/coverage.svg)](https://gitlab.com/youtube-tag-analyser/ytta-app/-/commits/main) [![api docs](https://img.shields.io/badge/api-docs-blue)](http://k8s-yttaapp-yttaappi-09ca915a8c-1517465418.eu-central-1.elb.amazonaws.com/docs)

*YouTube Tag Analyser App*

## Installation

```bash
pip install -r requirements.txt
pip install -r dev_requirements.txt
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
