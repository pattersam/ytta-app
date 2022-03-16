FROM python:3.8
COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD uvicorn --port 8000 main:app
