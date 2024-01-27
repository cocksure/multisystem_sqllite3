FROM python:3.9.11

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1

COPY requirements.txt /app/
WORKDIR /app
RUN python -m pip install --no-cache-dir -U pip
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

# Удаляем сгенерированные статические файлы
RUN rm -rf /app/static

# Копируем статику
COPY static /app/static

# Собираем статику
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "multisys.wsgi:application", "-b", "0.0.0.0:8000"]
