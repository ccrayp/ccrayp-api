# Gunicorn configuration
import multiprocessing

# Количество воркеров (для Render лучше 1-2)
workers = 1
# Или динамически based on CPU cores:
# workers = multiprocessing.cpu_count() * 2 + 1

# Количество потоков на воркер
threads = 4

# Таймауты (критически важно для Render)
timeout = 30  # секунд
graceful_timeout = 30
keepalive = 5

# Биндинг
bind = "0.0.0.0:10000"

# Логирование
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Перезапуск воркеров периодически (предотвращает утечки памяти)
max_requests = 1000
max_requests_jitter = 100