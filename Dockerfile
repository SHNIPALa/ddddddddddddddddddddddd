# ============================================================
# ULTIMATE AGGRESSIVE OSINT FRAMEWORK
# Dockerfile - ПОЛНАЯ РАБОЧАЯ ВЕРСИЯ
# ============================================================

FROM python:3.11-slim-bookworm

LABEL maintainer="OSINT Framework"
LABEL description="ULTIMATE AGGRESSIVE OSINT"
LABEL version="3.0.0"

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Базовые утилиты
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    git \
    curl \
    wget \
    ca-certificates \
    # Python
    python3-dev \
    python3-pip \
    # Библиотеки
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    # Документы
    poppler-utils \
    antiword \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-rus \
    # Архивы
    unzip \
    p7zip-full \
    unrar \
    # Сеть
    dnsutils \
    whois \
    nmap \
    tor \
    # Очистка
    && rm -rf /var/lib/apt/lists/*

# Установка локали
RUN apt-get update && apt-get install -y locales && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen && \
    rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Часовой пояс
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Создаем пользователя
RUN useradd -m -u 1000 -s /bin/bash osint && \
    mkdir -p /app /data /tmp/osint && \
    chown -R osint:osint /app /data /tmp/osint

WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Установка Python пакетов
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Загрузка NLTK данных
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); nltk.download('maxent_ne_chunker', quiet=True); nltk.download('words', quiet=True); nltk.download('vader_lexicon', quiet=True)" 2>/dev/null || true

# Загрузка spaCy моделей
RUN python -m spacy download en_core_web_sm 2>/dev/null || true && \
    python -m spacy download ru_core_news_sm 2>/dev/null || true

# Создаем директорию для GeoIP и скачиваем базы
RUN mkdir -p /usr/local/share/GeoIP && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb -O /usr/local/share/GeoIP/GeoLite2-City.mmdb 2>/dev/null || true && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb -O /usr/local/share/GeoIP/GeoLite2-ASN.mmdb 2>/dev/null || true

# Копируем код приложения
COPY --chown=osint:osint . .

# Создаем директории для данных
RUN mkdir -p /app/logs /app/reports /app/cache /app/uploads /app/exports && \
    chown -R osint:osint /app/logs /app/reports /app/cache /app/uploads /app/exports

# Переключаемся на пользователя
USER osint

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# Тома
VOLUME ["/data", "/app/logs", "/app/reports", "/app/cache", "/app/uploads", "/app/exports"]

# Команда запуска
CMD ["python", "Derty.py"]
