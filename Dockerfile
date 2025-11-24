# создаем основу
FROM python:3.13-slim AS builder
 
# создаем основную директорию
RUN mkdir /app
 
# устанавливаем рабочую директорию
WORKDIR /app
 
# устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
# устанавливаем зависимости
RUN pip install --upgrade pip 
COPY requirements.txt /app/ 
RUN pip install --no-cache-dir -r requirements.txt
 
# стадия продакшн
FROM python:3.13-slim
 
RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app
 
# копируем зависимости из основы
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
# устанавливаем рабочую директорию
WORKDIR /app
 
# копируем код приложения
COPY --chown=appuser:appuser . .
 
# устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
 
# открываем порт
EXPOSE 8000 
 
# запускаем приложение
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate --noinput && python -m gunicorn --bind 0.0.0.0:8000 --workers 3 mysite.wsgi:application"]