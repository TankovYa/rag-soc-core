```markdown
# Converter Service Kafka Events

## Обзор

Сервис Converter поддерживает **асинхронный запуск конвертации через Kafka**.  
Этот документ описывает все Kafka топики, форматы сообщений и примеры использования.

### Способы запуска

| Способ | Описание | Документация |
|--------|----------|--------------|
| **REST API** | Синхронный запуск, возвращает `job_id` | [OpenAPI Specification](./converter-api.yaml) |
| **Kafka** | Асинхронный запуск через `conversion.request` | Настоящий документ |

---

## Топики

| Топик | Тип | Описание |
|-------|-----|----------|
| `conversion.request` | Input | Запрос на запуск конвертации (асинхронный режим) |
| `conversion.request.error` | Output | Ошибки валидации запроса |
| `conversion.completed` | Output | Успешное завершение конвертации |
| `conversion.failed` | Output | Завершение с ошибкой |
| `conversion.cancelled` | Output | Отмена задачи |
| `conversion.progress` | Output | Промежуточные события прогресса (опционально) |

---

## 1. Запрос на конвертацию (Input Topic)

### Топик: `conversion.request`

Сообщение для асинхронного запуска конвертации. Позволяет запускать конвертацию без необходимости ожидания HTTP-ответа.

### Схема запроса

```json
{
  "request_id": "req_550e8400-e29b-41d4-a716-446655440000",
  "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
  "output_uri": "s3://bucket/output/platform_X_v2.1",
  "max_articles": null,
  "skip_extract": false,
  "log_level": 2,
  "reply_to": "conversion.response",
  "correlation_id": "corr_12345",
  "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
}
```

### Поля запроса

| Поле | Тип | Обязательный | Описание |
|------|-----|:-------------:|----------|
| `request_id` | string (UUID) | ✅ | Уникальный идентификатор запроса |
| `source_uri` | string | ✅ | Путь к исходному документу или папке (HDX, HTML, XML, PDF) |
| `output_uri` | string | ❌ | Выходная директория. По умолчанию: `{source_uri}_output` |
| `max_articles` | integer | ❌ | Обработать только первые N статей |
| `skip_extract` | boolean | ❌ | Пропустить извлечение HDX, использовать сохраненные HTML. По умолчанию: `false` |
| `log_level` | integer (0-3) | ❌ | Уровень логирования: 0=ERROR, 1=WARNING, 2=INFO, 3=DEBUG. По умолчанию: 2 |
| `reply_to` | string | ❌ | Топик для ответа о принятии задачи (если требуется подтверждение) |
| `correlation_id` | string | ❌ | Идентификатор для корреляции запроса и ответа |
| `traceparent` | string | ❌ | W3C Trace-Context для распределённой трассировки |

---

## 2. Ошибки валидации запроса

### Топик: `conversion.request.error`

Если запрос в Kafka не прошел валидацию, сервис отправляет сообщение об ошибке в этот топик.

### Схема ошибки

```json
{
  "request_id": "req_550e8400-e29b-41d4-a716-446655440000",
  "error": "Invalid source URI: URI cannot be empty",
  "code": "INVALID_SOURCE_URI",
  "details": {
    "field": "source_uri",
    "reason": "URI must be a valid path to file or directory"
  },
  "timestamp": "2024-03-25T10:00:00Z"
}
```

### Поля ошибки

| Поле | Тип | Описание |
|------|-----|----------|
| `request_id` | string | Идентификатор запроса (из исходного сообщения) |
| `error` | string | Человекочитаемое описание ошибки |
| `code` | string | Код ошибки для программной обработки |
| `details` | object | Дополнительные детали (какое поле, почему) |
| `timestamp` | string (ISO 8601) | Время возникновения ошибки |

### Коды ошибок

| Код | Описание |
|-----|----------|
| `INVALID_SOURCE_URI` | source_uri пуст или имеет неверный формат |
| `UNSUPPORTED_FORMAT` | Формат файла не поддерживается |
| `SOURCE_NOT_FOUND` | Указанный source_uri не существует или недоступен |
| `OUTPUT_URI_INVALID` | output_uri имеет неверный формат |
| `MAX_ARTICLES_INVALID` | max_articles не является положительным числом |
| `LOG_LEVEL_INVALID` | log_level вне диапазона 0-3 |

---

## 3. Ответ на запрос (если указан `reply_to`)

Если в запросе указан `reply_to`, сервис отправляет ответ о принятии задачи в указанный топик.

### Схема ответа

```json
{
  "request_id": "req_550e8400-e29b-41d4-a716-446655440000",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
  "output_uri": "s3://bucket/output/platform_X_v2.1",
  "created_at": "2024-03-25T10:00:00Z",
  "correlation_id": "corr_12345"
}
```

---

## 4. События завершения (Output Topics)

### 4.1 Успешное завершение

**Топик:** `conversion.completed`

```json
{
  "event_type": "conversion_completed",
  "request_id": "req_550e8400-e29b-41d4-a716-446655440000",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "source_uri": "s3://bucket/docs/platform_X.hdx",
  "output_uri": "s3://bucket/output/platform_X",
  "error_message": null,
  "warning_message": null,
  "statistics": {
    "conversion": {
      "total_html_files": 100,
      "total_topics": 100,
      "total_files": 500,
      "txt_files": 100,
      "md_files": 100,
      "metadata_files": 100,
      "html_backups": 100,
      "images_copied": 77,
      "tables_processed": 47,
      "internal_links_preserved": 112,
      "name_conflicts_resolved": 0,
      "errors_encountered": 0,
      "duration_seconds": 126.37
    },
    "validation": {
      "total_articles": 100,
      "valid_articles": 100,
      "articles_with_errors": 0,
      "articles_with_warnings": 73
    }
  },
  "started_at": "2024-03-25T10:00:05Z",
  "completed_at": "2024-03-25T10:02:05Z",
  "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
}
```

### 4.2 Завершение с ошибкой

**Топик:** `conversion.failed`

```json
{
  "event_type": "conversion_failed",
  "request_id": "req_550e8400-e29b-41d4-a716-446655440001",
  "job_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "failed",
  "source_uri": "s3://bucket/docs/corrupted.hdx",
  "output_uri": "s3://bucket/output/corrupted",
  "error_message": "Failed to parse HDX archive: invalid header at position 1024",
  "warning_message": null,
  "statistics": {
    "conversion": {
      "total_html_files": 23,
      "total_topics": 23,
      "total_files": 115,
      "txt_files": 23,
      "md_files": 23,
      "metadata_files": 23,
      "html_backups": 23,
      "images_copied": 12,
      "tables_processed": 8,
      "internal_links_preserved": 25,
      "name_conflicts_resolved": 0,
      "errors_encountered": 1,
      "duration_seconds": 28.3
    },
    "validation": {
      "total_articles": 23,
      "valid_articles": 23,
      "articles_with_errors": 1,
      "articles_with_warnings": 15
    }
  },
  "started_at": "2024-03-25T10:10:00Z",
  "completed_at": "2024-03-25T10:10:28Z",
  "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
}
```

### 4.3 Отмена задачи

**Топик:** `conversion.cancelled`

```json
{
  "event_type": "conversion_cancelled",
  "request_id": "req_550e8400-e29b-41d4-a716-446655440002",
  "job_id": "550e8400-e29b-41d4-a716-446655440002",
  "status": "cancelled",
  "source_uri": "s3://bucket/docs/large_doc.hdx",
  "output_uri": "s3://bucket/output/large_doc",
  "error_message": null,
  "warning_message": "Job cancelled by user",
  "statistics": {
    "conversion": {
      "total_html_files": 45,
      "total_topics": 45,
      "total_files": 225,
      "txt_files": 45,
      "md_files": 45,
      "metadata_files": 45,
      "html_backups": 45,
      "images_copied": 32,
      "tables_processed": 18,
      "internal_links_preserved": 51,
      "name_conflicts_resolved": 0,
      "errors_encountered": 0,
      "duration_seconds": 45.2
    },
    "validation": {
      "total_articles": 45,
      "valid_articles": 45,
      "articles_with_errors": 0,
      "articles_with_warnings": 28
    }
  },
  "started_at": "2024-03-25T10:15:00Z",
  "completed_at": "2024-03-25T10:15:45Z",
  "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
}
```

---

## 5. Промежуточные события прогресса (опционально)

**Топик:** `conversion.progress`

Для длительных конвертаций (более 10 минут) сервис может отправлять периодические сообщения о прогрессе.

```json
{
  "event_type": "conversion_progress",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "progress_percent": 45,
  "processed_articles": 45,
  "total_articles": 100,
  "timestamp": "2024-03-25T10:01:30Z"
}
```

---

## 6. Примеры отправки сообщений

### 6.1 Python (kafka-python)

```python
from kafka import KafkaProducer
import json
import uuid

producer = KafkaProducer(
    bootstrap_servers=['kafka.rag-system:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Запрос на конвертацию
request = {
    "request_id": str(uuid.uuid4()),
    "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
    "output_uri": "s3://bucket/output/platform_X_v2.1",
    "log_level": 2,
    "reply_to": "conversion.response",
    "correlation_id": "corr_12345",
    "traceparent": "00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
}

future = producer.send('conversion.request', value=request)
result = future.get(timeout=60)
print(f"Message sent: {result}")
```

### 6.2 Python (aiokafka) — асинхронный

```python
import asyncio
import json
import uuid
from aiokafka import AIOKafkaProducer

async def send_request():
    producer = AIOKafkaProducer(
        bootstrap_servers=['kafka.rag-system:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    
    try:
        request = {
            "request_id": str(uuid.uuid4()),
            "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
            "log_level": 2
        }
        await producer.send('conversion.request', value=request)
        print(f"Message sent: {request['request_id']}")
    finally:
        await producer.stop()

asyncio.run(send_request())
```

### 6.3 CLI (kcat / kafkacat)

```bash
echo '{
  "request_id": "req_550e8400-e29b-41d4-a716-446655440000",
  "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
  "log_level": 2
}' | kcat -P -b kafka.rag-system:9092 -t conversion.request
```

### 6.4 Consumer для получения результатов

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'conversion.completed',
    'conversion.failed',
    'conversion.cancelled',
    bootstrap_servers=['kafka.rag-system:9092'],
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

for message in consumer:
    event = message.value
    print(f"Event: {event['event_type']} - Job: {event['job_id']} - Status: {event['status']}")
    
    if event['status'] == 'completed':
        print(f"  Output: {event['output_uri']}")
        print(f"  Duration: {event['statistics']['conversion']['duration_seconds']}s")
    elif event['status'] == 'failed':
        print(f"  Error: {event['error_message']}")
```

---

## 7. Мониторинг и отладка

### Просмотр всех событий по job_id

```bash
# Подписка на все топики для конкретной задачи
kcat -C -b kafka.rag-system:9092 \
  -t conversion.completed \
  -t conversion.failed \
  -t conversion.cancelled \
  -o beginning \
  -J | jq 'select(.payload | contains("550e8400-e29b-41d4-a716-446655440000"))'
```

### Просмотр ошибок валидации

```bash
kcat -C -b kafka.rag-system:9092 -t conversion.request.error -o beginning -J | jq '.'
```

---

## 8. Конфигурация Kafka

| Параметр | Значение | Описание |
|----------|----------|----------|
| `bootstrap.servers` | `kafka.rag-system:9092` | Адрес Kafka кластера |
| `acks` | `all` | Подтверждение от всех реплик |
| `retries` | `10` | Количество попыток при ошибке |
| `enable.idempotence` | `true` | Гарантия exactly-once delivery |
| `compression.type` | `snappy` | Сжатие сообщений |
| `max.request.size` | `10485760` | Максимальный размер сообщения (10 MB) |

---

## 9. Сравнение подходов

| Характеристика | REST API | Kafka |
|----------------|----------|-------|
| **Синхронность** | Синхронный (возвращает job_id) | Асинхронный (неблокирующий) |
| **Ожидание ответа** | Немедленное получение job_id | Нет немедленного ответа (опционально через reply_to) |
| **Нагрузка** | Ограничена HTTP-сервером | Высокая пропускная способность |
| **Надежность** | Зависит от HTTP | At-least-once / exactly-once |
| **Backpressure** | Через HTTP 429 | Через партиции и consumer lag |
| **Use Case** | Ручной запуск, отладка | Автоматизированные пайплайны, ETL |

---

## 10. Порядок сообщений

1. **Запрос** → `conversion.request`
2. **При успешной валидации** → задача создаётся, начинается обработка
3. **При ошибке валидации** → `conversion.request.error`
4. **При завершении** → одно из сообщений: `conversion.completed`, `conversion.failed`, `conversion.cancelled`
5. **При длительной обработке** (опционально) → периодические `conversion.progress`

---

## 11. Полный пример: сквозной сценарий

```python
import asyncio
import json
import uuid
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

async def run_conversion():
    # 1. Отправка запроса
    producer = AIOKafkaProducer(
        bootstrap_servers=['kafka.rag-system:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    await producer.start()
    
    request_id = str(uuid.uuid4())
    request = {
        "request_id": request_id,
        "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
        "log_level": 2
    }
    
    await producer.send('conversion.request', value=request)
    print(f"Request sent: {request_id}")
    await producer.stop()
    
    # 2. Ожидание результата
    consumer = AIOKafkaConsumer(
        'conversion.completed',
        'conversion.failed',
        'conversion.cancelled',
        bootstrap_servers=['kafka.rag-system:9092'],
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    await consumer.start()
    
    try:
        async for msg in consumer:
            event = msg.value
            if event.get('request_id') == request_id:
                print(f"Result: {event['status']}")
                if event['status'] == 'completed':
                    print(f"  Output: {event['output_uri']}")
                elif event['status'] == 'failed':
                    print(f"  Error: {event['error_message']}")
                break
    finally:
        await consumer.stop()

asyncio.run(run_conversion())
```
```