FROM python:3.8
WORKDIR /code

# copy requirements first so caching speeds up build
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy remaining code
COPY ./app /code/app
COPY ./log-config.yaml /code/log-config.yaml

# Environment variables
ENV PROJECT_NAME="YouTube Tag Analyser"
ENV SERVER_NAME=0.0.0.0:8000
ENV SERVER_HOST=http://0.0.0.0
ENV BACKEND_CORS_ORIGINS='["http://k8s-yttaapp-yttaappf-636a1fff84-1865246281.eu-central-1.elb.amazonaws.com"]'
ENV FIRST_SUPERUSER=
ENV FIRST_SUPERUSER_PASSWORD=
ENV POSTGRES_SERVER=
ENV POSTGRES_DB=app
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=

# run server on port 8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config=log-config.yaml", "--proxy-headers"]
