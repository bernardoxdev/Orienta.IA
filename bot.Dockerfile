FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md /app/
RUN pip install --upgrade pip && pip install .

COPY bot.py .
COPY backend/core ./backend/core
COPY backend/database ./backend/database
COPY backend/messages ./backend/messages
COPY backend/utils ./backend/utils

CMD ["python", "-m", "bot"]