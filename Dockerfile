# ============================================================
# ULTIMATE AGGRESSIVE OSINT FRAMEWORK
# Dockerfile - С ИСПРАВЛЕНИЕМ libmagic
# ============================================================

FROM python:3.11-slim-bookworm

# Метаданные
LABEL maintainer="OSINT Framework"
LABEL description="ULTIMATE AGGRESSIVE OSINT"
LABEL version="2.0.1"

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
    # Python зависимости
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
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
    # 🔥 ВАЖНО: libmagic для python-magic
    libmagic-dev \
    libmagic1 \
    file \
    # Документы
    poppler-utils \
    antiword \
    unrtf \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-rus \
    # Базы данных
    libsqlite3-dev \
    libpq-dev \
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
    # SSL утилиты
    sslscan \
    # Мультимедиа
    ffmpeg \
    # Локали
    locales \
    tzdata \
    # Очистка кэша apt
    && rm -rf /var/lib/apt/lists/*

# 🔥 Создаем симлинк для libmagic (если нужно)
RUN if [ -f /usr/lib/x86_64-linux-gnu/libmagic.so.1 ]; then \
        ln -sf /usr/lib/x86_64-linux-gnu/libmagic.so.1 /usr/lib/libmagic.so; \
    elif [ -f /usr/lib/aarch64-linux-gnu/libmagic.so.1 ]; then \
        ln -sf /usr/lib/aarch64-linux-gnu/libmagic.so.1 /usr/lib/libmagic.so; \
    fi

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
COPY requirements.txt /app/requirements.txt

# 🔥 Установка Python пакетов с принудительной переустановкой python-magic
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    # Сначала устанавливаем python-magic отдельно
    pip install --no-cache-dir --force-reinstall python-magic && \
    pip install --no-cache-dir --force-reinstall python-magic-bin 2>/dev/null || true && \
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
    # Устанавливаем остальные пакеты из requirements с игнорированием ошибок
    if [ -f requirements.txt ] && [ -s requirements.txt ]; then \
        echo "=== Устанавливаем остальные зависимости ===" && \
        while IFS= read -r line || [ -n "$line" ]; do \
            [ -z "$line" ] && continue; \
            line=$(echo "$line" | sed 's/^\xEF\xBB\xBF//' | sed 's/^\xFF\xFE//' | sed 's/^\xFE\xFF//' | tr -d '\r\0' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//'); \
            [ -z "$line" ] && continue; \
            case "$line" in \#*) continue ;; esac; \
            # Пропускаем python-magic (уже установлен)
            if echo "$line" | grep -qi "python-magic"; then \
                echo "ℹ️ Пропускаем python-magic (уже установлен)"; \
                continue; \
            fi; \
            # Пропускаем системные пакеты
            if echo "$line" | grep -qiE '^(sslscan|sslyze|nmap|whois|tor|libmagic)'; then \
                echo "ℹ️ Пропускаем системный пакет: $line"; \
                continue; \
            fi; \
            echo "📦 Устанавливаем: $line"; \
            pip install --no-cache-dir "$line" 2>/dev/null || echo "⚠️ Не удалось установить $line (пропускаем)"; \
        done < requirements.txt; \
    fi && \
    echo "=== Проверка установки python-magic ===" && \
    python -c "import magic; print('✅ python-magic работает! Magic version:', magic.version)" || echo "❌ python-magic НЕ работает"

# 🔥 Проверка libmagic
RUN echo "=== Проверка системной libmagic ===" && \
    ldconfig -p | grep libmagic && \
    file --version && \
    ls -la /usr/lib/*/libmagic* 2>/dev/null || echo "libmagic files not found in standard location"

# Загрузка NLTK данных (опционально)
RUN python -c "import nltk; nltk.download('punkt', download_dir='/usr/local/share/nltk_data', quiet=True); nltk.download('stopwords', download_dir='/usr/local/share/nltk_data', quiet=True)" 2>/dev/null || echo "⚠️ NLTK download failed (non-critical)"

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
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/lib/aarch64-linux-gnu:$LD_LIBRARY_PATH

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import magic; import sys; sys.exit(0)" || exit 1

# Тома
VOLUME ["/data", "/app/logs", "/app/reports", "/app/cache", "/app/uploads", "/app/exports"]

# Команда запуска
CMD ["python", "Derty.py"]
