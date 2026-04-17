# ============================================================
# ULTIMATE AGGRESSIVE OSINT FRAMEWORK
# Dockerfile - БЕЗ ОШИБОК
# ============================================================

FROM python:3.11-slim-bookworm

LABEL maintainer="OSINT Framework"
LABEL description="ULTIMATE AGGRESSIVE OSINT"
LABEL version="4.0.1"

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    make \
    pkg-config \
    git \
    curl \
    wget \
    ca-certificates \
    python3-dev \
    python3-pip \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    libpoppler-dev \
    poppler-utils \
    antiword \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-rus \
    unzip \
    p7zip-full \
    unrar \
    dnsutils \
    whois \
    nmap \
    tor \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Локали
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

ENV LANG=en_US.UTF-8
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime

# Пользователь
RUN useradd -m -u 1000 -s /bin/bash osint && \
    mkdir -p /app /data /tmp/osint /opt/osint-tools && \
    chown -R osint:osint /app /data /tmp/osint /opt/osint-tools

WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Установка Python пакетов (с игнорированием ошибок для несуществующих)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    while IFS= read -r line || [ -n "$line" ]; do \
        [ -z "$line" ] && continue; \
        line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'); \
        [ -z "$line" ] && continue; \
        case "$line" in \#*) continue ;; esac; \
        echo "=== Устанавливаем: $line ===" && \
        pip install --no-cache-dir "$line" 2>/dev/null || echo "⚠️ Пропускаем: $line (не установлен)"; \
    done < requirements.txt

# Установка OSINT инструментов из GitHub
RUN cd /opt/osint-tools && \
    git clone --depth 1 https://github.com/laramies/theHarvester.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/sherlock-project/sherlock.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/p1ngul1n0/blackbird.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/megadose/toutatis.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/aboul3la/Sublist3r.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/darkoperator/dnsrecon.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/mschwager/fierce.git 2>/dev/null || true && \
    git clone --depth 1 https://github.com/guelfoweb/knock.git 2>/dev/null || true && \
    echo "✅ OSINT tools cloned"

ENV PATH="/opt/osint-tools/theHarvester:/opt/osint-tools/sherlock:/opt/osint-tools/blackbird:/opt/osint-tools/toutatis:/opt/osint-tools/Sublist3r:${PATH}"

# NLTK данные
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)" 2>/dev/null || true

# spaCy модели
RUN python -m spacy download en_core_web_sm 2>/dev/null || true

# GeoIP базы
RUN mkdir -p /usr/local/share/GeoIP && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb -O /usr/local/share/GeoIP/GeoLite2-City.mmdb 2>/dev/null || true

# Копируем код
COPY --chown=osint:osint . .

# Директории
RUN mkdir -p /app/logs /app/reports /app/cache /app/uploads /app/exports && \
    chown -R osint:osint /app/logs /app/reports /app/cache /app/uploads /app/exports

USER osint

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app:/opt/osint-tools

VOLUME ["/data", "/app/logs", "/app/reports"]

CMD ["python", "Derty.py"]
