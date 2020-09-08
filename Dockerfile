FROM python:3.8-slim

RUN apt-get update && apt-get install -y -qq libfreetype6 fontconfig-config

WORKDIR /app
COPY . .
ENV PIP_CONFIG_FILE /app/pip.conf

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD [ "gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app" ]
