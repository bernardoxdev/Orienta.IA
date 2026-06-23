FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md /app/
RUN pip install --upgrade pip && pip install .

EXPOSE 8000

COPY api.py .
COPY backend/core ./backend/core
COPY backend/database ./backend/database
COPY backend/events ./backend/events
COPY backend/routes ./backend/routes
COPY backend/services ./backend/services
COPY backend/utils ./backend/utils

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]