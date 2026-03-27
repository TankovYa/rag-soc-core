```markdown
# Примеры использования API Converter Service

## 1. Запуск конвертации

### 1.1 Конвертация HDX файла (базовый сценарий)

```bash
curl -X POST https://converter.rag-system.company.com/api/v1/convert \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01" \
  -H "Content-Type: application/json" \
  -d '{
    "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
    "output_uri": "s3://bucket/output/platform_X_v2.1",
    "log_level": 2
  }'
```

**Ответ:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
  "output_uri": "s3://bucket/output/platform_X_v2.1",
  "created_at": "2024-03-25T10:00:00Z"
}
```

### 1.2 Конвертация папки с документами (рекурсивно)

```bash
curl -X POST https://converter.rag-system.company.com/api/v1/convert \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01" \
  -H "Content-Type: application/json" \
  -d '{
    "source_uri": "s3://bucket/docs/platform_X/",
    "output_uri": "s3://bucket/output/platform_X_full",
    "log_level": 2
  }'
```

**Ответ:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "pending",
  "source_uri": "s3://bucket/docs/platform_X/",
  "output_uri": "s3://bucket/output/platform_X_full",
  "created_at": "2024-03-25T10:01:00Z"
}
```

### 1.3 Тестовый запуск (только первые 50 статей, DEBUG логирование)

```bash
curl -X POST https://converter-test.rag-system.company.com/api/v1/convert \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01" \
  -H "Content-Type: application/json" \
  -d '{
    "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
    "output_uri": "s3://bucket/output/platform_X_test",
    "max_articles": 50,
    "log_level": 3,
    "skip_extract": false
  }'
```

**Ответ:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440002",
  "status": "pending",
  "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
  "output_uri": "s3://bucket/output/platform_X_test",
  "created_at": "2024-03-25T10:02:00Z"
}
```

### 1.4 Конвертация с пропуском извлечения (использовать существующие HTML)

```bash
curl -X POST https://converter.rag-system.company.com/api/v1/convert \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01" \
  -H "Content-Type: application/json" \
  -d '{
    "source_uri": "s3://bucket/docs/platform_X/",
    "output_uri": "s3://bucket/output/platform_X_reprocess",
    "skip_extract": true,
    "log_level": 2
  }'
```

**Ответ:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440003",
  "status": "pending",
  "source_uri": "s3://bucket/docs/platform_X/",
  "output_uri": "s3://bucket/output/platform_X_reprocess",
  "created_at": "2024-03-25T10:03:00Z"
}
```

### 1.5 Конфликт: повторный запуск той же задачи

```bash
curl -X POST https://converter.rag-system.company.com/api/v1/convert \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01" \
  -H "Content-Type: application/json" \
  -d '{
    "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
    "log_level": 2
  }'
```

**Ответ (409 Conflict):**
```json
{
  "error": "Job already exists for this source_uri",
  "code": "JOB_ALREADY_EXISTS",
  "details": {
    "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
    "existing_job_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "request_id": "req_abc127",
  "trace_id": "0af7651916cd43dd8448eb211c80319c"
}
```

---

## 2. Получение списка задач

### 2.1 Получить все задачи

```bash
curl -X GET https://converter.rag-system.company.com/api/v1/convert \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

**Ответ:**
```json
{
  "jobs": [
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
      "output_uri": "s3://bucket/output/platform_X_v2.1",
      "created_at": "2024-03-25T10:00:00Z",
      "started_at": "2024-03-25T10:00:05Z",
      "completed_at": "2024-03-25T10:02:05Z"
    },
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440001",
      "status": "processing",
      "source_uri": "s3://bucket/docs/platform_X/",
      "output_uri": "s3://bucket/output/platform_X_full",
      "created_at": "2024-03-25T10:01:00Z",
      "started_at": "2024-03-25T10:01:10Z",
      "completed_at": null
    }
  ],
  "total": 4,
  "limit": 50,
  "offset": 0
}
```

### 2.2 Получить только завершенные задачи

```bash
curl -X GET "https://converter.rag-system.company.com/api/v1/convert?status=completed&limit=10" \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

**Ответ:**
```json
{
  "jobs": [
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440000",
      "status": "completed",
      "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
      "output_uri": "s3://bucket/output/platform_X_v2.1",
      "created_at": "2024-03-25T10:00:00Z",
      "completed_at": "2024-03-25T10:02:05Z"
    }
  ],
  "total": 1,
  "limit": 10,
  "offset": 0
}
```

### 2.3 Получить задачи с пагинацией

```bash
curl -X GET "https://converter.rag-system.company.com/api/v1/convert?limit=2&offset=2" \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

**Ответ:**
```json
{
  "jobs": [
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440002",
      "status": "failed",
      "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
      "output_uri": "s3://bucket/output/platform_X_test",
      "created_at": "2024-03-25T10:02:00Z",
      "completed_at": "2024-03-25T10:02:33Z"
    },
    {
      "job_id": "550e8400-e29b-41d4-a716-446655440003",
      "status": "cancelled",
      "source_uri": "s3://bucket/docs/platform_X/",
      "output_uri": "s3://bucket/output/platform_X_reprocess",
      "created_at": "2024-03-25T10:03:00Z",
      "completed_at": "2024-03-25T10:04:15Z"
    }
  ],
  "total": 4,
  "limit": 2,
  "offset": 2
}
```

---

## 3. Получение статуса задачи

### 3.1 Статус задачи в процессе обработки

```bash
curl -X GET https://converter.rag-system.company.com/api/v1/convert/550e8400-e29b-41d4-a716-446655440001/status \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

**Ответ:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "processing",
  "progress_percent": 45,
  "source_uri": "s3://bucket/docs/platform_X/",
  "output_uri": "s3://bucket/output/platform_X_full",
  "error_message": null,
  "warning_message": null,
  "statistics": null,
  "started_at": "2024-03-25T10:01:10Z",
  "completed_at": null
}
```

### 3.2 Статус завершенной задачи (с полной статистикой)

```bash
curl -X GET https://converter.rag-system.company.com/api/v1/convert/550e8400-e29b-41d4-a716-446655440000/status \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

**Ответ:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress_percent": 100,
  "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
  "output_uri": "s3://bucket/output/platform_X_v2.1",
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
  "completed_at": "2024-03-25T10:02:05Z"
}
```

### 3.3 Статус задачи с предупреждениями

```bash
curl -X GET https://converter.rag-system.company.com/api/v1/convert/550e8400-e29b-41d4-a716-446655440005/status \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

**Ответ:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440005",
  "status": "completed",
  "progress_percent": 100,
  "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
  "output_uri": "s3://bucket/output/platform_X_v2.1",
  "error_message": null,
  "warning_message": "73 articles had warnings: missing images, broken links, unsupported HTML tags",
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
  "started_at": "2024-03-25T10:05:05Z",
  "completed_at": "2024-03-25T10:07:11Z"
}
```

### 3.4 Статус задачи, завершенной с ошибкой

```bash
curl -X GET https://converter.rag-system.company.com/api/v1/convert/550e8400-e29b-41d4-a716-446655440002/status \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

**Ответ:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440002",
  "status": "failed",
  "progress_percent": 23,
  "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
  "output_uri": "s3://bucket/output/platform_X_test",
  "error_message": "Failed to parse HDX archive: invalid header at position 1024. Archive appears corrupted.",
  "warning_message": null,
  "statistics": {
    "conversion": {
      "total_html_files": 115,
      "total_topics": 115,
      "total_files": 575,
      "txt_files": 115,
      "md_files": 115,
      "metadata_files": 115,
      "html_backups": 115,
      "images_copied": 89,
      "tables_processed": 54,
      "internal_links_preserved": 129,
      "name_conflicts_resolved": 0,
      "errors_encountered": 1,
      "duration_seconds": 28.3
    },
    "validation": {
      "total_articles": 115,
      "valid_articles": 115,
      "articles_with_errors": 1,
      "articles_with_warnings": 84
    }
  },
  "started_at": "2024-03-25T10:02:10Z",
  "completed_at": "2024-03-25T10:02:38Z"
}
```

### 3.5 Задача не найдена

```bash
curl -X GET https://converter.rag-system.company.com/api/v1/convert/00000000-0000-0000-0000-000000000000/status \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

**Ответ (404 Not Found):**
```json
{
  "error": "Job not found",
  "code": "JOB_NOT_FOUND",
  "details": {
    "job_id": "00000000-0000-0000-0000-000000000000"
  },
  "request_id": "req_abc126",
  "trace_id": "0af7651916cd43dd8448eb211c80319c"
}
```

---

## 4. Отмена задачи

### 4.1 Успешная отмена выполняющейся задачи

```bash
curl -X POST https://converter.rag-system.company.com/api/v1/convert/550e8400-e29b-41d4-a716-446655440001/cancel \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

**Ответ:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440001",
  "status": "cancelled",
  "message": "Job cancelled successfully"
}
```

### 4.2 Попытка отмены уже завершенной задачи

```bash
curl -X POST https://converter.rag-system.company.com/api/v1/convert/550e8400-e29b-41d4-a716-446655440000/cancel \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

**Ответ (409 Conflict):**
```json
{
  "error": "Cannot cancel job: job already completed",
  "code": "JOB_ALREADY_COMPLETED",
  "details": {
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed"
  },
  "request_id": "req_abc128",
  "trace_id": "0af7651916cd43dd8448eb211c80319c"
}
```

### 4.3 Попытка отмены уже отмененной задачи

```bash
curl -X POST https://converter.rag-system.company.com/api/v1/convert/550e8400-e29b-41d4-a716-446655440003/cancel \
  -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"
```

**Ответ (409 Conflict):**
```json
{
  "error": "Cannot cancel job: job already cancelled",
  "code": "JOB_ALREADY_CANCELLED",
  "details": {
    "job_id": "550e8400-e29b-41d4-a716-446655440003",
    "status": "cancelled"
  },
  "request_id": "req_abc129",
  "trace_id": "0af7651916cd43dd8448eb211c80319c"
}
```

---

## 5. Health Checks (для Kubernetes)

### 5.1 Liveness probe

```bash
curl -X GET https://converter.rag-system.company.com/health
```

**Ответ (сервис здоров):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "components": {}
}
```

### 5.2 Readiness probe (все зависимости доступны)

```bash
curl -X GET https://converter.rag-system.company.com/ready
```

**Ответ (сервис готов):**
```json
{
  "ready": true,
  "checks": {
    "object_storage": true,
    "kafka": true
  }
}
```

### 5.3 Readiness probe (Kafka недоступна)

```bash
curl -X GET https://converter.rag-system.company.com/ready
```

**Ответ (сервис не готов — 503 Service Unavailable):**
```json
{
  "ready": false,
  "checks": {
    "object_storage": true,
    "kafka": false
  }
}
```

---

## 6. Prometheus метрики

### 6.1 Получение метрик

```bash
curl -X GET https://converter.rag-system.company.com/metrics
```

**Ответ:**
```
# HELP converter_requests_total Total number of requests
# TYPE converter_requests_total counter
converter_requests_total{method="POST",endpoint="/convert"} 42
converter_requests_total{method="GET",endpoint="/convert/status"} 156
converter_requests_total{method="GET",endpoint="/convert"} 23
converter_requests_total{method="POST",endpoint="/convert/cancel"} 5

# HELP converter_requests_duration_seconds Request duration in seconds
# TYPE converter_requests_duration_seconds histogram
converter_requests_duration_seconds_bucket{method="POST",endpoint="/convert",le="0.1"} 35
converter_requests_duration_seconds_bucket{method="POST",endpoint="/convert",le="0.5"} 42
converter_requests_duration_seconds_bucket{method="POST",endpoint="/convert",le="1.0"} 42
converter_requests_duration_seconds_bucket{method="POST",endpoint="/convert",le="+Inf"} 42
converter_requests_duration_seconds_sum{method="POST",endpoint="/convert"} 8.5
converter_requests_duration_seconds_count{method="POST",endpoint="/convert"} 42

# HELP converter_errors_total Total number of errors
# TYPE converter_errors_total counter
converter_errors_total{code="JOB_NOT_FOUND"} 3
converter_errors_total{code="INVALID_SOURCE_URI"} 2
converter_errors_total{code="JOB_ALREADY_COMPLETED"} 1

# HELP converter_jobs_total Total number of conversion jobs
# TYPE converter_jobs_total counter
converter_jobs_total{status="pending"} 5
converter_jobs_total{status="processing"} 3
converter_jobs_total{status="completed"} 28
converter_jobs_total{status="failed"} 4
converter_jobs_total{status="cancelled"} 2

# HELP converter_jobs_duration_seconds Job duration in seconds
# TYPE converter_jobs_duration_seconds histogram
converter_jobs_duration_seconds_bucket{le="30"} 8
converter_jobs_duration_seconds_bucket{le="60"} 15
converter_jobs_duration_seconds_bucket{le="120"} 22
converter_jobs_duration_seconds_bucket{le="300"} 25
converter_jobs_duration_seconds_bucket{le="+Inf"} 28
converter_jobs_duration_seconds_sum 1842.5
converter_jobs_duration_seconds_count 28

# HELP converter_active_jobs Currently active jobs
# TYPE converter_active_jobs gauge
converter_active_jobs 3
```

---

## 7. Автоматизация с помощью скриптов

### 7.1 Bash скрипт: запуск и ожидание завершения

```bash
#!/bin/bash

# Конфигурация
API_URL="https://converter.rag-system.company.com"
TRACEPARENT="00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01"

# Запуск конвертации
response=$(curl -s -X POST "${API_URL}/api/v1/convert" \
  -H "traceparent: ${TRACEPARENT}" \
  -H "Content-Type: application/json" \
  -d '{
    "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
    "log_level": 2
  }')

job_id=$(echo $response | jq -r '.job_id')
echo "Job started: $job_id"

# Ожидание завершения
while true; do
  status_response=$(curl -s "${API_URL}/api/v1/convert/${job_id}/status" \
    -H "traceparent: ${TRACEPARENT}")
  
  status=$(echo $status_response | jq -r '.status')
  progress=$(echo $status_response | jq -r '.progress_percent')
  
  echo "[$(date +%H:%M:%S)] Status: $status, Progress: $progress%"
  
  if [ "$status" == "completed" ] || [ "$status" == "failed" ] || [ "$status" == "cancelled" ]; then
    break
  fi
  
  sleep 5
done

echo "Final status: $status"
echo $status_response | jq '.'
```

### 7.2 Python скрипт: мониторинг с callback

```python
import requests
import time
import uuid
from typing import Optional, Callable
from datetime import datetime


class ConverterClient:
    """Клиент для работы с Converter Service API."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.traceparent = f"00-{uuid.uuid4().hex}-{uuid.uuid4().hex[:16]}-01"
    
    def convert(
        self,
        source_uri: str,
        output_uri: Optional[str] = None,
        max_articles: Optional[int] = None,
        skip_extract: bool = False,
        log_level: int = 2
    ) -> str:
        """Запуск конвертации."""
        payload = {
            "source_uri": source_uri,
            "skip_extract": skip_extract,
            "log_level": log_level
        }
        if output_uri:
            payload["output_uri"] = output_uri
        if max_articles:
            payload["max_articles"] = max_articles
        
        response = requests.post(
            f"{self.base_url}/api/v1/convert",
            json=payload,
            headers={"traceparent": self.traceparent}
        )
        response.raise_for_status()
        return response.json()["job_id"]
    
    def get_status(self, job_id: str) -> dict:
        """Получение статуса задачи."""
        response = requests.get(
            f"{self.base_url}/api/v1/convert/{job_id}/status",
            headers={"traceparent": self.traceparent}
        )
        response.raise_for_status()
        return response.json()
    
    def wait_for_completion(
        self,
        job_id: str,
        timeout: int = 3600,
        poll_interval: int = 5,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> dict:
        """
        Ожидание завершения задачи.
        
        Args:
            job_id: Идентификатор задачи
            timeout: Таймаут в секундах
            poll_interval: Интервал опроса в секундах
            progress_callback: Callback для прогресса
        
        Returns:
            Финальный статус задачи
        """
        start_time = time.time()
        last_progress = -1
        
        while time.time() - start_time < timeout:
            status = self.get_status(job_id)
            current_progress = status.get("progress_percent", 0)
            
            if progress_callback and current_progress != last_progress:
                progress_callback(current_progress)
                last_progress = current_progress
            
            if status["status"] in ["completed", "failed", "cancelled"]:
                return status
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Job {job_id} did not complete within {timeout} seconds")
    
    def cancel(self, job_id: str) -> dict:
        """Отмена задачи."""
        response = requests.post(
            f"{self.base_url}/api/v1/convert/{job_id}/cancel",
            headers={"traceparent": self.traceparent}
        )
        response.raise_for_status()
        return response.json()
    
    def list_jobs(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> dict:
        """Получение списка задач."""
        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        
        response = requests.get(
            f"{self.base_url}/api/v1/convert",
            params=params,
            headers={"traceparent": self.traceparent}
        )
        response.raise_for_status()
        return response.json()


# Пример использования с callback для прогресса
def on_progress(percent: int):
    """Callback для отображения прогресса."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Progress: {percent}%")


def main():
    client = ConverterClient("https://converter.rag-system.company.com")
    
    # Запуск конвертации
    print("Starting conversion...")
    job_id = client.convert(
        source_uri="s3://bucket/docs/platform_X_v2.1.hdx",
        log_level=2
    )
    print(f"Job ID: {job_id}")
    
    # Ожидание завершения с мониторингом прогресса
    try:
        result = client.wait_for_completion(
            job_id,
            timeout=3600,
            progress_callback=on_progress
        )
        
        if result["status"] == "completed":
            stats = result["statistics"]["conversion"]
            print(f"\n✅ Conversion completed successfully!")
            print(f"   HTML files: {stats['total_html_files']}")
            print(f"   Duration: {stats['duration_seconds']:.2f}s")
            print(f"   Output: {result['output_uri']}")
        elif result["status"] == "failed":
            print(f"\n❌ Conversion failed: {result['error_message']}")
        else:
            print(f"\n⚠️ Conversion {result['status']}")
            
    except TimeoutError as e:
        print(f"\n⏰ Timeout: {e}")
    except requests.exceptions.RequestException as e:
        print(f"\n🚨 API error: {e}")


if __name__ == "__main__":
    main()
```

### 7.3 Python скрипт: массовая обработка

```python
import asyncio
import aiohttp
from typing import List, Dict
import uuid


class AsyncConverterClient:
    """Асинхронный клиент для массовой обработки."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    async def convert(
        self,
        session: aiohttp.ClientSession,
        source_uri: str,
        output_uri: Optional[str] = None,
        log_level: int = 2
    ) -> str:
        """Асинхронный запуск конвертации."""
        traceparent = f"00-{uuid.uuid4().hex}-{uuid.uuid4().hex[:16]}-01"
        
        payload = {
            "source_uri": source_uri,
            "log_level": log_level
        }
        if output_uri:
            payload["output_uri"] = output_uri
        
        async with session.post(
            f"{self.base_url}/api/v1/convert",
            json=payload,
            headers={"traceparent": traceparent}
        ) as response:
            data = await response.json()
            return data["job_id"]
    
    async def get_status(
        self,
        session: aiohttp.ClientSession,
        job_id: str
    ) -> dict:
        """Асинхронное получение статуса."""
        async with session.get(
            f"{self.base_url}/api/v1/convert/{job_id}/status"
        ) as response:
            return await response.json()
    
    async def process_batch(
        self,
        sources: List[Dict[str, str]]
    ) -> List[Dict]:
        """
        Массовая обработка документов.
        
        Args:
            sources: Список словарей с ключами 'source_uri' и опционально 'output_uri'
        
        Returns:
            Результаты обработки
        """
        results = []
        
        async with aiohttp.ClientSession() as session:
            # Запуск всех конвертаций
            jobs = []
            for source in sources:
                job_id = await self.convert(
                    session,
                    source["source_uri"],
                    source.get("output_uri")
                )
                jobs.append({
                    "job_id": job_id,
                    "source_uri": source["source_uri"]
                })
                print(f"Started: {source['source_uri']} -> {job_id}")
            
            # Мониторинг всех задач
            pending = jobs.copy()
            while pending:
                for job in pending[:]:
                    status = await self.get_status(session, job["job_id"])
                    
                    if status["status"] in ["completed", "failed", "cancelled"]:
                        job["result"] = status
                        results.append(job)
                        pending.remove(job)
                        print(f"Completed: {job['source_uri']} - {status['status']}")
                
                if pending:
                    await asyncio.sleep(5)
        
        return results


async def main():
    client = AsyncConverterClient("https://converter.rag-system.company.com")
    
    sources = [
        {"source_uri": "s3://bucket/docs/product_A.hdx"},
        {"source_uri": "s3://bucket/docs/product_B.hdx"},
        {"source_uri": "s3://bucket/docs/product_C.hdx"},
        {"source_uri": "s3://bucket/docs/product_D.hdx"},
    ]
    
    results = await client.process_batch(sources)
    
    print("\n=== Summary ===")
    completed = [r for r in results if r["result"]["status"] == "completed"]
    failed = [r for r in results if r["result"]["status"] == "failed"]
    
    print(f"Total: {len(results)}")
    print(f"Completed: {len(completed)}")
    print(f"Failed: {len(failed)}")
    
    for job in failed:
        print(f"  - {job['source_uri']}: {job['result']['error_message']}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 8. Интеграция с Kafka (ожидаемое сообщение)

После завершения конвертации сервис отправляет сообщение в Kafka топик `conversion.completed`:

```json
{
  "event_type": "conversion_completed",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "source_uri": "s3://bucket/docs/platform_X_v2.1.hdx",
  "output_uri": "s3://bucket/output/platform_X_v2.1",
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

### Пример потребителя Kafka

```python
from kafka import KafkaConsumer
import json


def consume_conversion_events():
    """Потребитель событий конвертации."""
    consumer = KafkaConsumer(
        'conversion.completed',
        'conversion.failed',
        'conversion.cancelled',
        bootstrap_servers=['kafka.rag-system:9092'],
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    
    print("Waiting for conversion events...")
    
    for message in consumer:
        event = message.value
        event_type = event.get('event_type', 'unknown')
        job_id = event.get('job_id')
        status = event.get('status')
        
        print(f"\n[{event_type}] Job: {job_id}")
        print(f"  Status: {status}")
        print(f"  Source: {event.get('source_uri')}")
        print(f"  Output: {event.get('output_uri')}")
        
        if status == 'completed':
            stats = event.get('statistics', {}).get('conversion', {})
            print(f"  Duration: {stats.get('duration_seconds', 0):.2f}s")
            print(f"  Files: {stats.get('total_files', 0)}")
        elif status == 'failed':
            print(f"  Error: {event.get('error_message')}")


if __name__ == "__main__":
    consume_conversion_events()
```

---

## 9. Коды ошибок

| Код | Описание | HTTP статус |
|-----|----------|-------------|
| `INVALID_SOURCE_URI` | source_uri пуст или имеет неверный формат | 400 |
| `UNSUPPORTED_FORMAT` | Формат файла не поддерживается | 400 |
| `MAX_ARTICLES_INVALID` | max_articles не является положительным числом | 400 |
| `LOG_LEVEL_INVALID` | log_level вне диапазона 0-3 | 400 |
| `JOB_ALREADY_EXISTS` | Задача с таким source_uri уже существует | 409 |
| `JOB_NOT_FOUND` | Задача не найдена | 404 |
| `JOB_ALREADY_COMPLETED` | Невозможно отменить уже завершенную задачу | 409 |
| `JOB_ALREADY_CANCELLED` | Невозможно отменить уже отмененную задачу | 409 |
| `CANCEL_FAILED` | Не удалось отменить задачу | 409 |
| `OBJECT_STORAGE_UNAVAILABLE` | Object Storage недоступен | 503 |
| `KAFKA_UNAVAILABLE` | Kafka недоступна | 503 |
```