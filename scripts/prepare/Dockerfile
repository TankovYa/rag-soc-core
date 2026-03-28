FROM python:3.11-slim

LABEL maintainer="RAG System Team"
LABEL description="HDX Converter Service for RAG Platform"

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование requirements.txt
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY hdx_converter/ ./hdx_converter/

# Создание непривилегированного пользователя
RUN useradd -m -u 1000 converter && chown -R converter:converter /app
USER converter

# Экспорт порта
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Запуск API сервера
ENTRYPOINT ["python", "-m", "hdx_converter.cli", "api"]
CMD ["--host", "0.0.0.0", "--port", "8080"]