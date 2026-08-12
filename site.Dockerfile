FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md /app/
RUN pip install --upgrade pip && pip install .

EXPOSE 5000

COPY web.py .
COPY frontend/ ./frontend/

CMD ["gunicorn", "-b", "0.0.0.0:5000", "web:app"]