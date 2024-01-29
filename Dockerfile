FROM python:3.9

RUN apt-get update \
    && apt-get install -y nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -U pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m pip cache purge \
    && rm -rf /root/.cache

RUN rm -rf /var/cache/nginx/*

EXPOSE 8030

CMD ["gunicorn", "multisys.wsgi:application", "-b", "0.0.0.0:8030"]
