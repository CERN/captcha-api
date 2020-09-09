# Captcha API

This project contains a simple Captcha API that returns an encoded image containing
letters a-Z and numbers 1-9 via a GET endpoint. The POST endpoint can be used to validate the
captcha.

A Dockerfile is provided for containerisation.

## Running with Docker

Build the Docker image
```
docker build . -t captcha-api
```

Run the Docker image
```
docker run -d --name captcha -p 8080:8080 -e CAPTCHA_API_CONFIG=config.py captcha-api
```

Navigate to ``http://localhost:8080/swagger-ui``
