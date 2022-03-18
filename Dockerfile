FROM python:3.8
WORKDIR /code

# copy requirements first so caching speeds up build
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy remaining code
COPY ./app /code/app
COPY ./log-config.yaml /code/log-config.yaml

# run server on port 8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config=log-config.yaml", "--proxy-headers"]
