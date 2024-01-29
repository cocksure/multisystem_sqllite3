FROM python:3.9.11


SHELL ["/bin/bash", "-c"]


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1


COPY requirements.txt /app/
WORKDIR /app
RUN python -m pip install --no-cache-dir -U pip
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8030

CMD ["gunicorn", "multisys.wsgi:application", "-b", "0.0.0.0:8030"]
