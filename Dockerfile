FROM python:3.11-slim

WORKDIR /app

COPY privacy_ms.py /app
COPY helper.py /app
COPY requirements.txt /app
COPY certs /app/certs/

RUN pip install -r requirements.txt \
    pip install "uvicorn[standard]"

EXPOSE 8000

CMD ["uvicorn", "privacy_ms:app", "--host", "0.0.0.0", "--reload", "--ssl-keyfile", "certs/geraldyong-priv.pem", "--ssl-certfile", "certs/geraldyong-cert.pem"]
