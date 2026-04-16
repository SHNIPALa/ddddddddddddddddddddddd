FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    find /usr/local/lib/python3.11/site-packages -name "*.pyc" -delete

COPY bot.py .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

CMD ["python", "-u", "bot.py"]
