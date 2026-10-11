FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir "Flask>=3.1,<4.0" "psycopg[binary]>=3.2,<4.0" "gunicorn>=23.0,<24.0"

COPY api/api.py .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "api:app"]