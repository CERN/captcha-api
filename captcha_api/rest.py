import time
from base64 import b64encode
from datetime import datetime, timedelta
from uuid import uuid4
from wsgiref import headers

from flask import request, send_file
from flask_restx import Api, Resource, fields

from .captcha_generator import CaptchaGenerator
from .db import db
from .lang_best_match import best_locale
from .models import Captcha
from .speech import text_to_speech
from .speech_gtts import text_to_speech as tts_gtts


WAIT_TIME = 2

api = Api(
    title="CAPTCHA API",
    description="A simple API for handling CAPTCHA",
    security={"oauth2": ["api"]},
    doc="/swagger-ui",
)


captcha_ns = api.namespace(
    "captcha", description="Utilities for validating and generating CAPTCHA"
)


captcha_model = captcha_ns.model(
    "CaptchaAnswer", {"answer": fields.String, "id": fields.String}
)


def get_request_data(request):
    """
    Gets the data from the request
    """
    # https://stackoverflow.com/questions/10434599/how-to-get-data-received-in-flask-request/25268170
    data = request.form.to_dict() if request.form else request.get_json()
    if not data:
        return {}
    return data


@captcha_ns.route("/")
class CaptchaResource(Resource):
    """
    Handling captchas
    """

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api=api, *args, **kwargs)
        self.generator = CaptchaGenerator(
            fontname=api.app.config["DEFAULT_CAPTCHA_FONT"]
        )

    def get(self):
        """
        Generate a new captcha text
        """

        # Slow generation in case of attack
        time.sleep(WAIT_TIME)

        img_array, answer = self.generator.generate_captcha()
        captcha_id = str(uuid4())
        new_captcha = Captcha(id=captcha_id, answer=answer)
        db.session.add(new_captcha)
        db.session.commit()
        return {
            "id": captcha_id,
            "img": "data:image/jpeg;base64," + b64encode(img_array.getvalue()).decode(),
        }

    @captcha_ns.doc(body=captcha_model)
    def post(self):
        """
        Solve a captcha and match it with the database thing
        """
        data = get_request_data(request)

        existing = Captcha.query.filter_by(id=data["id"]).first()
        if not existing:
            return {"message": "Not found"}, 404

        time_difference = datetime.utcnow() - existing.creation_time
        if time_difference > timedelta(minutes=1):
            db.session.delete(existing)
            db.session.commit()
            return {"message": "You did not answer fast enough!"}, 400

        if data["answer"].casefold() != existing.answer.casefold():
            db.session.delete(existing)
            db.session.commit()
            return {"message": "Invalid answer"}, 400

        db.session.delete(existing)
        db.session.commit()
        return {"message": "Valid"}


@captcha_ns.route("/audio/<string:captcha_id>")
class CaptchaAudioResource(Resource):
    """
    Sending audio recordings for captchas
    """

    def get(self, captcha_id):
        """
        Generate a audio captcha with local tts engine (offline)
        Language based on header 'Accept-Language' following https://datatracker.ietf.org/doc/html/rfc3282
        e.g: Headers 'Accept-Language: es-ES
        """

        # Slow generation in case of attack
        time.sleep(WAIT_TIME)

        if request.accept_languages:
            lang = best_locale(request.accept_languages)
        else:
            lang = "en"

        existing_captcha = Captcha.query.get_or_404(captcha_id)
        split_answer = ", ".join(existing_captcha.answer)
        mp3_file = text_to_speech(split_answer, lang)

        return send_file(
            mp3_file,
            as_attachment=True,
            cache_timeout=-1,
            attachment_filename="captcha.mp3",
            mimetype="audio/mpeg",
        )


@captcha_ns.route("/audio/gtts/<string:captcha_id>")
class CaptchaAudioResourceGtts(Resource):
    """
    Sending audio recordings for captchas with Google tts
    """

    def get(self, captcha_id):
        """
        Generate a audio captcha with google tts
        Language based on header 'Accept-Language' following https://datatracker.ietf.org/doc/html/rfc3282
        e.g: Headers 'Accept-Language: es-ES
        """

        if request.accept_languages:
            lang = best_locale(request.accept_languages)
        else:
            lang = "en"

        existing_captcha = Captcha.query.get_or_404(captcha_id)
        split_answer = ", ".join(existing_captcha.answer)
        mp3_file = tts_gtts(split_answer, lang)

        return send_file(
            mp3_file,
            as_attachment=True,
            cache_timeout=-1,
            attachment_filename="captcha.mp3",
            mimetype="audio/mpeg",
        )
