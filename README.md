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

## Running locally

This guide is written for users of Debian-based systems, the package names might differ on other operating systems such as CentOS.

For usage on Windows, please use the WSL2 distribution in order to build and run the application.

### Installing the required libraries

Unfortunately we need some binary dependencies, since PIL and the audio CAPTCHA generation require them. Run the following command:

```bash
sudo apt-get install libtiff5-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev ffmpeg espeak python3-dev
```

### Installing and running the application

Run

```bash
pip install -e '.[dev]'
```

in order to install all the required dependencies for development.

To start the server locally, you need to create a `captcha.cfg` file. Just `cp captcha_api/captcha.cfg.example captcha_api/captcha.cfg` to get started.

Running the server is done by running:

```
flask run
```

or

```
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

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


## Embedded captcha.js

The Captcha API includes a static Javascript file to help with simple web form integrations. To use or test this script:

1. Configure the `captchaApiUrl` variable in `captcha_api/static/captcha.js`.
2. Run the Captcha API.
3. Include the script in your page, and the HTML element `<div id="cern-captcha"></div>` in your form (see the example in `captcha_api/static/demo.html`).
4. When processing your form, validate `captchaAnswer` and `captchaId` with the `POST` endpoint of the Captcha API.

Example for the production Captcha API:

```
<!DOCTYPE html>
<html>
    <script type="module" src="https://captcha.web.cern.ch/static/captcha.js"></script>
<body>
    <form>
        <div id="cern-captcha"></div>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
```


## Deploy on our AWS cluster

### Retrieve the current tag on padam-k8s repo


```
cat captcha-api/values.yml
```

### Push the image to ECR with

```
./push_docker_image.sh -t CURRENT_TAG + 1
```

### Deploy the new image using padam-k8s

To set the new version, edit

```
captcha-api/values.yml
git add captcha-api/values.yml
git commit -m "Update captcha-api"
git push
```

Wait ~2 minutes for Argo to deploy the new version
