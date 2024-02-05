FROM python:3.9

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1
ENV XDG_RUNTIME_DIR=/tmp/runtime-root

# Установка зависимостей для wkhtmltopdf
RUN apt-get update && \
    apt-get install -y wkhtmltopdf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
WORKDIR /app
RUN python -m pip install --no-cache-dir -U pip
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8030

CMD ["python", "manage.py", "runserver", "0.0.0.0:8030"]
#CMD ["gunicorn", "multisys.wsgi:application", "-b", "0.0.0.0:8030"]
