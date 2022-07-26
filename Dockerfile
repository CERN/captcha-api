FROM docker.io/library/python:3.10-slim

RUN apt-get update && apt-get install -y -qq libfreetype6 fontconfig-config espeak espeak-data ffmpeg libtiff5-dev libopenjp2-7-dev zlib1g-dev python3-tk gcc libfreetype6-dev

WORKDIR /app
COPY . .
ENV PIP_CONFIG_FILE /app/pip.conf

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD [ "gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app" ]
