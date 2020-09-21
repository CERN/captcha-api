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
docker run -d --name captcha -p 8080:8080 -e CAPTCHA_API_CONFIG=captcha.cfg captcha-api
```

Navigate to `http://localhost:8080/swagger-ui`

## Audio CAPTCHA

For accessibility reasons, one might one to listen to the CAPTCHA message. In order to do yhat, you can point to the following endpoint:

```
/api/v1.0/captcha/audio/$CAPTCHA_ID
```

The file returned is in the `mp3` format and can be easily loaded into an HTML form as such:

```html
<div>
  <audio controls="controls" className="audio-element">
    <source src="http://localhost:8080/api/v1.0/captcha/audio/$CAPTCHA_ID" } />
  </audio>
</div>
```


## Running migrations

Make sure you installed the dependencies using `pip install -e .`. 

Afterwards, run `flask db upgrade` to bring your DB to the latest level. By default it will use a `test.db` SQLite file in the `captcha_api` folder.
