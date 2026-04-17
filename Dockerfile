# ============================================================
# ULTIMATE AGGRESSIVE OSINT FRAMEWORK
# Dockerfile - Полное окружение для максимальной разведки
# ============================================================

FROM python:3.11-slim-bookworm

# Метаданные
LABEL maintainer="OSINT Framework"
LABEL description="ULTIMATE AGGRESSIVE OSINT - Выжимаем все соки!"
LABEL version="1.0.0"

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Базовые утилиты
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    automake \
    autoconf \
    libtool \
    pkg-config \
    git \
    curl \
    wget \
    ca-certificates \
    gnupg \
    apt-transport-https \
    software-properties-common \
    # Python зависимости для сборки
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    cython3 \
    # Библиотеки для криптографии и SSL
    libssl-dev \
    libffi-dev \
    libsasl2-dev \
    libldap2-dev \
    libcurl4-openssl-dev \
    # XML и HTML парсинг
    libxml2-dev \
    libxslt1-dev \
    libxml2-utils \
    # Изображения
    libjpeg-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    libimage-exiftool-perl \
    exiftool \
    # Документы
    libmagic-dev \
    libmagic1 \
    poppler-utils \
    antiword \
    unrtf \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-rus \
    # Базы данных
    libsqlite3-dev \
    libpq-dev \
    libmariadb-dev \
    # Архивы
    unzip \
    p7zip-full \
    p7zip-rar \
    rar \
    unrar \
    lz4 \
    zstd \
    # Сеть и DNS
    dnsutils \
    bind9-dnsutils \
    whois \
    nmap \
    net-tools \
    iputils-ping \
    traceroute \
    tor \
    torsocks \
    proxychains4 \
    # Мультимедиа
    ffmpeg \
    # Прочее
    locales \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Установка локали
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Установка часового пояса
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Создаем пользователя без root прав
RUN useradd -m -u 1000 -s /bin/bash osint && \
    mkdir -p /app /data /tmp/osint && \
    chown -R osint:osint /app /data /tmp/osint

# Рабочая директория
WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Установка Python пакетов
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Установка дополнительных пакетов через git
RUN pip install --no-cache-dir \
    git+https://github.com/laramies/theHarvester.git \
    git+https://github.com/sherlock-project/sherlock.git \
    git+https://github.com/megadose/holehe.git \
    git+https://github.com/soxoj/maigret.git \
    git+https://github.com/p1ngul1n0/blackbird.git \
    git+https.com/nexfil/nexfil.git

# Загрузка NLTK данных
RUN python -c "import nltk; nltk.download('punkt', download_dir='/usr/local/share/nltk_data'); nltk.download('stopwords', download_dir='/usr/local/share/nltk_data'); nltk.download('averaged_perceptron_tagger', download_dir='/usr/local/share/nltk_data'); nltk.download('maxent_ne_chunker', download_dir='/usr/local/share/nltk_data'); nltk.download('words', download_dir='/usr/local/share/nltk_data'); nltk.download('vader_lexicon', download_dir='/usr/local/share/nltk_data')"

# Загрузка spaCy моделей
RUN python -m spacy download en_core_web_sm && \
    python -m spacy download ru_core_news_sm

# Установка geolite2 баз
RUN mkdir -p /usr/local/share/GeoIP && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb -O /usr/local/share/GeoIP/GeoLite2-City.mmdb && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb -O /usr/local/share/GeoIP/GeoLite2-ASN.mmdb && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-Country.mmdb -O /usr/local/share/GeoIP/GeoLite2-Country.mmdb

# Копируем код приложения
COPY --chown=osint:osint . .

# Создаем директории для данных
RUN mkdir -p /app/logs /app/reports /app/cache /app/uploads /app/exports && \
    chown -R osint:osint /app/logs /app/reports /app/cache /app/uploads /app/exports

# Копируем конфигурационные файлы
COPY docker/config.torrc /etc/tor/torrc 2>/dev/null || true
COPY docker/proxychains.conf /etc/proxychains4.conf 2>/dev/null || true

# Устанавливаем права
RUN chmod +x /app/*.py 2>/dev/null || true

# Переключаемся на пользователя
USER osint

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app
ENV TOR_SOCKS_PORT=9050
ENV TOR_CONTROL_PORT=9051

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Тома для постоянных данных
VOLUME ["/data", "/app/logs", "/app/reports", "/app/cache", "/app/uploads", "/app/exports"]

# Открываем порты (если нужен веб-интерфейс)
EXPOSE 8000 8080

# Команда запуска
CMD ["python", "bot.py"]
