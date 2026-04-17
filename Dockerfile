# ============================================================
# ULTIMATE AGGRESSIVE OSINT FRAMEWORK
# Dockerfile - ПОЛНАЯ ВЕРСИЯ СО ВСЕМИ ИНСТРУМЕНТАМИ
# ============================================================

FROM python:3.11-slim-bookworm

LABEL maintainer="OSINT Framework"
LABEL description="ULTIMATE AGGRESSIVE OSINT - ALL IMPORTS WORKING"
LABEL version="4.0.0"

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Компиляция
    build-essential \
    gcc \
    g++ \
    make \
    cmake \
    pkg-config \
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
    # PDF/Poppler
    libpoppler-dev \
    libpoppler-cpp-dev \
    poppler-utils \
    # Документы
    antiword \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-rus \
    # Архивы
    unzip \
    p7zip-full \
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
    # Chromium для selenium
    chromium \
    chromium-driver \
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
    mkdir -p /app /data /tmp/osint /opt/osint-tools && \
    chown -R osint:osint /app /data /tmp/osint /opt/osint-tools

WORKDIR /app

# Копируем requirements
COPY requirements.txt .

# Установка Python пакетов
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# ============================================================
# УСТАНОВКА OSINT ИНСТРУМЕНТОВ ИЗ GIT
# ============================================================

RUN cd /opt/osint-tools && \
    # theHarvester
    git clone --depth 1 https://github.com/laramies/theHarvester.git && \
    cd theHarvester && pip install -r requirements.txt . && cd .. && \
    # Sherlock
    git clone --depth 1 https://github.com/sherlock-project/sherlock.git && \
    cd sherlock && pip install -r requirements.txt && cd .. && \
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
    # EmailRep
    git clone --depth 1 https://github.com/keraattin/EmailRep.git && \
    cd EmailRep && pip install -r requirements.txt && cd .. && \
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
    # Ahmia
    git clone --depth 1 https://github.com/ahmia/ahmia-site.git && \
    # IPFS Search
    git clone --depth 1 https://github.com/ipfs-search/ipfs-search.git && \
    echo "All OSINT tools installed"

# Добавляем инструменты в PATH
ENV PATH="/opt/osint-tools/theHarvester:/opt/osint-tools/sherlock:/opt/osint-tools/blackbird:/opt/osint-tools/nexfil:/opt/osint-tools/toutatis:/opt/osint-tools/GHunt:/opt/osint-tools/Sublist3r:/opt/osint-tools/dnsrecon:/opt/osint-tools/fierce:/opt/osint-tools/knock:${PATH}"

# Загрузка NLTK данных
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); nltk.download('maxent_ne_chunker', quiet=True); nltk.download('words', quiet=True); nltk.download('vader_lexicon', quiet=True)" 2>/dev/null || true

# Загрузка spaCy моделей
RUN python -m spacy download en_core_web_sm 2>/dev/null || true && \
    python -m spacy download ru_core_news_sm 2>/dev/null || true

# Создаем директорию для GeoIP
RUN mkdir -p /usr/local/share/GeoIP && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb -O /usr/local/share/GeoIP/GeoLite2-City.mmdb 2>/dev/null || true && \
    wget -q https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb -O /usr/local/share/GeoIP/GeoLite2-ASN.mmdb 2>/dev/null || true

# Копируем код приложения
COPY --chown=osint:osint . .

# Создаем директории
RUN mkdir -p /app/logs /app/reports /app/cache /app/uploads /app/exports && \
    chown -R osint:osint /app/logs /app/reports /app/cache /app/uploads /app/exports

# Переключаемся на пользователя
USER osint

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app:/opt/osint-tools

# Тома
VOLUME ["/data", "/app/logs", "/app/reports", "/app/cache", "/app/uploads", "/app/exports"]

# Команда запуска
CMD ["python", "Derty.py"]
