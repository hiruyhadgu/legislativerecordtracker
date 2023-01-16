# backend/Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /fastapi

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /fastapi

CMD uvicorn compute:app --host=0.0.0.0 --port=$PORT