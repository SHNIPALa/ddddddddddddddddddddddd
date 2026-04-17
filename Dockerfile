# ============================================================
# ULTIMATE AGGRESSIVE OSINT FRAMEWORK
# Dockerfile - ИСПРАВЛЕННАЯ ВЕРСИЯ (с pdftotext зависимостями)
# ============================================================

FROM python:3.11-slim-bookworm

LABEL maintainer="OSINT Framework"
LABEL description="ULTIMATE AGGRESSIVE OSINT"
LABEL version="3.0.1"

# Установка системных зависимостей (ВКЛЮЧАЯ ВСЁ ДЛЯ КОМПИЛЯЦИИ)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Базовые утилиты для компиляции
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    pkg-config \
    automake \
    autoconf \
    libtool \
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
    # 🔥 PDF и Poppler (для pdftotext)
    libpoppler-dev \
    libpoppler-cpp-dev \
    poppler-utils \
    pkg-config \
    # Документы
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
    # Локали
    locales \
    # Очистка
    && rm -rf /var/lib/apt/lists/*

# Установка локали
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

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
    # Устанавливаем пакеты по одному с обработкой ошибок
    for pkg in \
        "aiogram>=3.0.0" \
        "aiohttp>=3.9.0" \
        "python-dotenv>=1.0.0" \
        "phonenumbers>=8.13.0" \
        "dnspython>=2.4.0" \
        "email-validator>=2.1.0" \
        "python-whois>=0.8.0" \
        "pyOpenSSL>=23.3.0" \
        "cryptography>=41.0.0" \
        "certifi>=2023.11.17" \
        "geoip2>=4.7.0" \
        "maxminddb>=2.4.0" \
        "geopy>=2.4.0" \
        "Pillow>=10.1.0" \
        "exifread>=3.0.0" \
        "filetype>=1.2.0" \
        "pdfplumber>=0.10.0" \
        "docx2txt>=0.8" \
        "python-docx>=1.1.0" \
        "openpyxl>=3.1.0" \
        "python-pptx>=0.6.23" \
        "olefile>=0.47" \
        "textract>=1.6.5" \
        "rarfile>=4.1" \
        "py7zr>=0.20.0" \
        "beautifulsoup4>=4.12.0" \
        "lxml>=4.9.0" \
        "requests>=2.31.0" \
        "shodan>=1.31.0" \
        "vt-py>=0.18.0" \
        "waybackpy>=3.0.0" \
        "nltk>=3.8.0" \
        "spacy>=3.7.0" \
        "langdetect>=1.0.9" \
        "googletrans>=4.0.0" \
        "networkx>=3.2.0" \
        "pandas>=2.1.0" \
        "numpy>=1.26.0" \
        "python-dateutil>=2.8.0" \
        "dateparser>=1.2.0" \
        "pytz>=2023.3" \
        "click>=8.1.0" \
        "rich>=13.7.0" \
        "tqdm>=4.66.0" \
        "colorama>=0.4.6" \
        "pyyaml>=6.0.0" \
        "bcrypt>=4.1.0" \
        "pycryptodome>=3.19.0" \
        "web3>=6.14.0" \
        "urllib3>=2.0.0" \
        "chardet>=5.0.0"; \
    do \
        echo "=== Устанавливаем: $pkg ===" && \
        pip install --no-cache-dir "$pkg" 2>/dev/null || echo "⚠️ Предупреждение: не удалось установить $pkg"; \
    done && \
    # 🔥 pdftotext устанавливаем ОТДЕЛЬНО с флагами для компиляции
    echo "=== Устанавливаем pdftotext (требует компиляции) ===" && \
    CFLAGS="-I/usr/include/poppler" LDFLAGS="-L/usr/lib" pip install --no-cache-dir pdftotext 2>/dev/null || \
    echo "⚠️ pdftotext не установлен (будет использован pdfplumber)"

# Загрузка NLTK данных
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); nltk.download('maxent_ne_chunker', quiet=True); nltk.download('words', quiet=True)" 2>/dev/null || true

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
