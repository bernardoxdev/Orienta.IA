FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md /app/
RUN pip install --upgrade pip && pip install .

EXPOSE 5000

COPY web.py .
COPY backend/core ./backend/core
COPY backend/database ./backend/database
COPY backend/services ./backend/services
COPY backend/utils ./backend/utils

CMD ["gunicorn", "-b", "0.0.0.0:5000", "web:app"]
