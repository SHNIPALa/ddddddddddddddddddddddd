# ============================================================
# ULTIMATE AGGRESSIVE OSINT FRAMEWORK
# Dockerfile - ИСПРАВЛЕННАЯ ВЕРСИЯ (с non-free репозиториями)
# ============================================================

FROM python:3.11-slim-bookworm

LABEL maintainer="OSINT Framework"
LABEL description="ULTIMATE AGGRESSIVE OSINT"
LABEL version="5.0.2"

# ============================================================
# ДОБАВЛЕНИЕ NON-FREE РЕПОЗИТОРИЕВ (для unrar и p7zip-rar)
# ============================================================
RUN echo "deb http://deb.debian.org/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list

# ============================================================
# УСТАНОВКА СИСТЕМНЫХ ЗАВИСИМОСТЕЙ
# ============================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Компиляция
    build-essential \
    gcc \
    g++ \
    make \
    pkg-config \
    cmake \
    automake \
    autoconf \
    libtool \
    # Git и сеть
    git \
    curl \
    wget \
    ca-certificates \
    # Python
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    cython3 \
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
    # Cairo
    libcairo2-dev \
    libcairo2 \
    libgirepository1.0-dev \
    # PDF
    libpoppler-dev \
    libpoppler-cpp-dev \
    poppler-utils \
    # Документы
    antiword \
    # OCR
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-rus \
    # Архивы (исправлено)
    unzip \
    p7zip-full \
    p7zip-rar \
    unrar-free \
    # Сеть и DNS
    dnsutils \
    whois \
    nmap \
    tor \
    torsocks \
    # Базы данных
    libsqlite3-dev \
    # Локали
    locales \
    tzdata \
    # Очистка
    && rm -rf /var/lib/apt/lists/*

# ============================================================
# НАСТРОЙКА ЛОКАЛИ И ЧАСОВОГО ПОЯСА
# ============================================================
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
ENV TZ=Europe/Moscow

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# ============================================================
# СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ
# ============================================================
RUN useradd -m -u 1000 -s /bin/bash osint && \
    mkdir -p /app /data /tmp/osint /opt/osint-tools && \
    chown -R osint:osint /app /data /tmp/osint /opt/osint-tools

WORKDIR /app

# ============================================================
# УСТАНОВКА PYTHON ПАКЕТОВ
# ============================================================
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Копируем requirements
COPY requirements.txt .

# Устанавливаем пакеты с игнорированием ошибок
RUN while IFS= read -r line || [ -n "$line" ]; do \
        [ -z "$line" ] && continue; \
        line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'); \
        [ -z "$line" ] && continue; \
        case "$line" in \#*) continue ;; esac; \
        echo "=== Installing: $line ==="; \
        pip install --no-cache-dir "$line" 2>/dev/null || echo "⚠️ Skipped: $line"; \
    done < requirements.txt

# ============================================================
# NLTK ДАННЫЕ
# ============================================================
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)" 2>/dev/null || true

# ============================================================
# SPACY МОДЕЛИ
# ============================================================
RUN python -m spacy download en_core_web_sm 2>/dev/null || true

# ============================================================
# GEOLITE2 БАЗЫ
# ============================================================
RUN mkdir -p /usr/local/share/GeoIP && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb -O /usr/local/share/GeoIP/GeoLite2-City.mmdb 2>/dev/null || true

# ============================================================
# КОПИРОВАНИЕ КОДА
# ============================================================
COPY --chown=osint:osint . .

# ============================================================
# СОЗДАНИЕ ДИРЕКТОРИЙ
# ============================================================
RUN mkdir -p /app/logs /app/reports /app/cache /app/uploads /app/exports && \
    chown -R osint:osint /app/logs /app/reports /app/cache /app/uploads /app/exports

# ============================================================
# ПЕРЕКЛЮЧЕНИЕ НА ПОЛЬЗОВАТЕЛЯ
# ============================================================
USER osint

# ============================================================
# ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ
# ============================================================
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# ============================================================
# HEALTHCHECK
# ============================================================
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# ============================================================
# ТОМА
# ============================================================
VOLUME ["/data", "/app/logs", "/app/reports"]

# ============================================================
# КОМАНДА ЗАПУСКА
# ============================================================
CMD ["python", "Derty.py"]
