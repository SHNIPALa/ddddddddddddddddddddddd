# ============================================================
# ULTIMATE AGGRESSIVE OSINT FRAMEWORK
# Dockerfile - ИСПРАВЛЕННАЯ ВЕРСИЯ
# ============================================================

FROM python:3.11-slim-bookworm

# Метаданные
LABEL maintainer="OSINT Framework"
LABEL description="ULTIMATE AGGRESSIVE OSINT - Выжимаем все соки!"
LABEL version="2.0.0"

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
    # SSL утилиты (СИСТЕМНЫЕ, НЕ PYTHON!)
    sslscan \
    sslyze \
    testssl.sh \
    # Мультимедиа
    ffmpeg \
    # Прочее
    locales \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Установка testssl.sh (если не установился через apt)
RUN if ! command -v testssl &> /dev/null; then \
        git clone --depth 1 https://github.com/drwetter/testssl.sh.git /opt/testssl && \
        ln -s /opt/testssl/testssl.sh /usr/local/bin/testssl; \
    fi

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

# Копируем ИСПРАВЛЕННЫЙ requirements.txt
COPY requirements-fixed.txt /app/requirements.txt

# Установка Python пакетов (с обработкой ошибок)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    # Устанавливаем критически важные пакеты
    pip install --no-cache-dir \
        aiogram>=3.0.0 \
        aiohttp>=3.9.0 \
        python-dotenv>=1.0.0 \
        phonenumbers>=8.13.0 \
        dnspython>=2.4.0 \
        python-whois>=0.8.0 \
        Pillow>=10.1.0 \
        beautifulsoup4>=4.12.0 \
        requests>=2.31.0 \
        email-validator>=2.1.0 \
        pyOpenSSL>=23.3.0 \
        cryptography>=41.0.0 \
        certifi>=2023.11.17 \
    && \
    # Устанавливаем остальные из requirements с игнорированием ошибок
    if [ -f requirements.txt ] && [ -s requirements.txt ]; then \
        echo "=== Устанавливаем остальные зависимости ===" && \
        while IFS= read -r line || [ -n "$line" ]; do \
            [ -z "$line" ] && continue; \
            line=$(echo "$line" | sed 's/^\xEF\xBB\xBF//' | sed 's/^\xFF\xFE//' | sed 's/^\xFE\xFF//' | tr -d '\r\0' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'); \
            [ -z "$line" ] && continue; \
            case "$line" in \#*) continue ;; esac; \
            # Пропускаем системные пакеты
            if echo "$line" | grep -qiE '^(sslscan|sslyze|nmap|whois|tor)'; then \
                echo "ℹ️ Пропускаем системный пакет: $line"; \
                continue; \
            fi; \
            # Пропускаем встроенные модули Python
            if echo "$line" | grep -qiE '^(sqlite3|json|os|sys|time|datetime|re|random|math|logging|asyncio|collections|itertools|functools|operator|pathlib|urllib|http|socket|ssl|hashlib|base64|uuid|threading|multiprocessing|queue|concurrent|subprocess|shutil|tempfile|pickle|copy|weakref|gc|ctypes|struct|array|binascii|codecs|encodings|locale|gettext|argparse|configparser|csv|io|textwrap|string|unicodedata)$'; then \
                echo "ℹ️ Пропускаем встроенный модуль: $line"; \
                continue; \
            fi; \
            echo "📦 Устанавливаем: $line"; \
            pip install --no-cache-dir "$line" 2>/dev/null || echo "⚠️ Не удалось установить $line (пропускаем)"; \
        done < requirements.txt; \
    fi && \
    echo "=== Установка завершена ==="

# Загрузка NLTK данных (с обработкой ошибок)
RUN python -c "import nltk; nltk.download('punkt', download_dir='/usr/local/share/nltk_data', quiet=True); nltk.download('stopwords', download_dir='/usr/local/share/nltk_data', quiet=True); nltk.download('averaged_perceptron_tagger', download_dir='/usr/local/share/nltk_data', quiet=True)" 2>/dev/null || echo "⚠️ NLTK download failed (non-critical)"

# Загрузка spaCy моделей (с обработкой ошибок)
RUN python -m spacy download en_core_web_sm 2>/dev/null || echo "⚠️ spaCy model download failed (non-critical)" && \
    python -m spacy download ru_core_news_sm 2>/dev/null || echo "⚠️ spaCy RU model download failed (non-critical)"

# Установка geolite2 баз
RUN mkdir -p /usr/local/share/GeoIP && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb -O /usr/local/share/GeoIP/GeoLite2-City.mmdb 2>/dev/null || echo "⚠️ GeoIP download failed" && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb -O /usr/local/share/GeoIP/GeoLite2-ASN.mmdb 2>/dev/null || echo "⚠️ GeoIP ASN download failed"

# Копируем код приложения
COPY --chown=osint:osint . .

# Создаем директории для данных
RUN mkdir -p /app/logs /app/reports /app/cache /app/uploads /app/exports && \
    chown -R osint:osint /app/logs /app/reports /app/cache /app/uploads /app/exports

# Устанавливаем права на Python файлы
RUN find /app -name "*.py" -exec chmod +x {} \; 2>/dev/null || true

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

# Команда запуска
CMD ["python", "bot.py"]
