FROM python:3.10-slim

WORKDIR /app

COPY routers/router.py .
COPY hosts ./hosts
COPY utils ./utils
COPY config ./config

CMD ["python", "router.py"]
