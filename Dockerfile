# ============================================================
# ULTIMATE AGGRESSIVE OSINT FRAMEWORK
# Dockerfile - ПОЛНАЯ ВЕРСИЯ
# ============================================================

FROM python:3.11-slim-bookworm

LABEL maintainer="OSINT Framework"
LABEL description="ULTIMATE AGGRESSIVE OSINT - Maximum data extraction"
LABEL version="5.0.0"

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
    libopenjp2-7-dev \
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
    bind9-dnsutils \
    whois \
    nmap \
    net-tools \
    iputils-ping \
    traceroute \
    # Tor и прокси
    tor \
    torsocks \
    proxychains4 \
    # Базы данных
    libsqlite3-dev \
    libpq-dev \
    # Локали
    locales \
    tzdata \
    # Очистка кэша apt
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
# СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ (БЕЗ ROOT)
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
# УСТАНОВКА PYTHON ПАКЕТОВ
# ============================================================
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# ============================================================
# УСТАНОВКА OSINT ИНСТРУМЕНТОВ ИЗ GITHUB
# ============================================================
RUN cd /opt/osint-tools && \
    # theHarvester
    git clone --depth 1 https://github.com/laramies/theHarvester.git && \
    cd theHarvester && pip install -r requirements.txt . && cd .. && \
    # Sherlock
    git clone --depth 1 https://github.com/sherlock-project/sherlock.git && \
    cd sherlock && pip install -r requirements.txt && cd .. && \
    # Holehe
    git clone --depth 1 https://github.com/megadose/holehe.git && \
    cd holehe && pip install -r requirements.txt . && cd .. && \
    # Maigret
    git clone --depth 1 https://github.com/soxoj/maigret.git && \
    cd maigret && pip install -r requirements.txt . && cd .. && \
    # Blackbird
    git clone --depth 1 https://github.com/p1ngul1n0/blackbird.git && \
    cd blackbird && pip install -r requirements.txt && cd .. && \
    # Nexfil
    git clone --depth 1 https://github.com/thewhiteh4t/nexfil.git && \
    cd nexfil && pip install -r requirements.txt && cd .. && \
    # Toutatis
    git clone --depth 1 https://github.com/megadose/toutatis.git && \
    cd toutatis && pip install -r requirements.txt . && cd .. && \
    # Ghunt
    git clone --depth 1 https://github.com/mxrch/GHunt.git && \
    cd GHunt && pip install -r requirements.txt && cd .. && \
    # Sublist3r
    git clone --depth 1 https://github.com/aboul3la/Sublist3r.git && \
    cd Sublist3r && pip install -r requirements.txt && cd .. && \
    # DNSRecon
    git clone --depth 1 https://github.com/darkoperator/dnsrecon.git && \
    cd dnsrecon && pip install -r requirements.txt && cd .. && \
    # Fierce
    git clone --depth 1 https://github.com/mschwager/fierce.git && \
    cd fierce && pip install -r requirements.txt && cd .. && \
    # Knockpy
    git clone --depth 1 https://github.com/guelfoweb/knock.git && \
    cd knock && pip install -r requirements.txt && cd .. && \
    # OnionSearch
    git clone --depth 1 https://github.com/megadose/OnionSearch.git && \
    cd OnionSearch && pip install -r requirements.txt && cd .. && \
    # DarkSearch
    git clone --depth 1 https://github.com/thewhiteh4t/DarkSearch.git && \
    cd DarkSearch && pip install -r requirements.txt && cd .. && \
    echo "✅ All OSINT tools installed"

# ============================================================
# ДОБАВЛЕНИЕ ИНСТРУМЕНТОВ В PATH
# ============================================================
ENV PATH="/opt/osint-tools/theHarvester:/opt/osint-tools/sherlock:/opt/osint-tools/holehe:/opt/osint-tools/maigret:/opt/osint-tools/blackbird:/opt/osint-tools/nexfil:/opt/osint-tools/toutatis:/opt/osint-tools/GHunt:/opt/osint-tools/Sublist3r:/opt/osint-tools/dnsrecon:/opt/osint-tools/fierce:/opt/osint-tools/knock:${PATH}"

# ============================================================
# ЗАГРУЗКА NLTK ДАННЫХ
# ============================================================
RUN python -c "import nltk; nltk.download('punkt', download_dir='/usr/local/share/nltk_data', quiet=True); nltk.download('stopwords', download_dir='/usr/local/share/nltk_data', quiet=True); nltk.download('averaged_perceptron_tagger', download_dir='/usr/local/share/nltk_data', quiet=True); nltk.download('maxent_ne_chunker', download_dir='/usr/local/share/nltk_data', quiet=True); nltk.download('words', download_dir='/usr/local/share/nltk_data', quiet=True); nltk.download('vader_lexicon', download_dir='/usr/local/share/nltk_data', quiet=True)" 2>/dev/null || true

# ============================================================
# ЗАГРУЗКА SPACY МОДЕЛЕЙ
# ============================================================
RUN python -m spacy download en_core_web_sm 2>/dev/null || true && \
    python -m spacy download ru_core_news_sm 2>/dev/null || true

# ============================================================
# ЗАГРУЗКА GEOLITE2 БАЗ
# ============================================================
RUN mkdir -p /usr/local/share/GeoIP && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb -O /usr/local/share/GeoIP/GeoLite2-City.mmdb 2>/dev/null || true && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb -O /usr/local/share/GeoIP/GeoLite2-ASN.mmdb 2>/dev/null || true && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-Country.mmdb -O /usr/local/share/GeoIP/GeoLite2-Country.mmdb 2>/dev/null || true

# ============================================================
# КОПИРОВАНИЕ КОДА
# ============================================================
COPY --chown=osint:osint . .

# ============================================================
# СОЗДАНИЕ ДИРЕКТОРИЙ ДЛЯ ДАННЫХ
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
ENV TOR_SOCKS_PORT=9050
ENV TOR_CONTROL_PORT=9051

# ============================================================
# HEALTHCHECK
# ============================================================
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# ============================================================
# ТОМА
# ============================================================
VOLUME ["/data", "/app/logs", "/app/reports", "/app/cache", "/app/uploads", "/app/exports"]

# ============================================================
# КОМАНДА ЗАПУСКА
# ============================================================
CMD ["python", "Derty.py"]
