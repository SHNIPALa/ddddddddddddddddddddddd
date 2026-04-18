# ============================================================
# ULTIMATE AGGRESSIVE OSINT FRAMEWORK
# Dockerfile - ИСПРАВЛЕННАЯ ВЕРСИЯ (с pycairo зависимостями)
# ============================================================

FROM python:3.11-slim-bookworm

LABEL maintainer="OSINT Framework"
LABEL description="ULTIMATE AGGRESSIVE OSINT"
LABEL version="5.0.1"

# ============================================================
# УСТАНОВКА СИСТЕМНЫХ ЗАВИСИМОСТЕЙ
# ============================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Компиляция (ОБЯЗАТЕЛЬНО для pycairo)
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
    # Библиотеки для криптографии
    libssl-dev \
    libffi-dev \
    # XML и HTML
    libxml2-dev \
    libxslt1-dev \
    # Изображения
    libjpeg-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    # 🔥 CAIRO (для pycairo/maigret)
    libcairo2-dev \
    libcairo2 \
    python3-cairo \
    python3-cairo-dev \
    libgirepository1.0-dev \
    gir1.2-gtk-3.0 \
    # PDF
    libpoppler-dev \
    libpoppler-cpp-dev \
    poppler-utils \
    # Документы
    antiword \
    unrtf \
    # OCR
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-rus \
    # Архивы
    unzip \
    p7zip-full \
    p7zip-rar \
    unrar \
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
# КОПИРОВАНИЕ requirements.txt
# ============================================================
COPY requirements.txt .

# ============================================================
# УСТАНОВКА PYTHON ПАКЕТОВ (с обработкой ошибок)
# ============================================================
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Устанавливаем пакеты по одному, игнорируя ошибки
RUN while IFS= read -r line || [ -n "$line" ]; do \
        [ -z "$line" ] && continue; \
        line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'); \
        [ -z "$line" ] && continue; \
        case "$line" in \#*) continue ;; esac; \
        echo "=== Installing: $line ==="; \
        pip install --no-cache-dir "$line" 2>/dev/null || echo "⚠️ Skipped: $line"; \
    done < requirements.txt

# 🔥 Отдельно устанавливаем pycairo (требует системные библиотеки)
RUN pip install --no-cache-dir pycairo 2>/dev/null || echo "⚠️ pycairo not installed"

# ============================================================
# УСТАНОВКА OSINT ИНСТРУМЕНТОВ (опционально)
# ============================================================
RUN cd /opt/osint-tools && \
    git clone --depth 1 https://github.com/laramies/theHarvester.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/sherlock-project/sherlock.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/megadose/holehe.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/p1ngul1n0/blackbird.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/thewhiteh4t/nexfil.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/megadose/toutatis.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/aboul3la/Sublist3r.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/darkoperator/dnsrecon.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/mschwager/fierce.git 2>/dev/null || true && \
    echo "✅ OSINT tools cloned"

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
ENV PYTHONPATH=/app:/opt/osint-tools

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
