import time
from base64 import b64encode
from datetime import datetime, timedelta
from uuid import uuid4
import logging

from flask import request, send_file
from flask_restx import Api, Resource, fields

from .captcha_generator import CaptchaGenerator
from .db import db
from .lang_best_match import best_locale
from .models import Captcha
from .speech import text_to_speech
from .speech_gtts import text_to_speech as tts_gtts
from .starfleetipdefender import is_ip_blacklisted

# Currently front is not able to handle a wait...
WAIT_TIME = 0.5

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
        captcha_id = str(uuid4())
        
        if is_ip_blacklisted(ip=request.remote_addr):
            logging.error(f"{request.remote_addr} is blacklisted send a fake captcha")
            return {
                "id": captcha_id,
                "img": "data:image/jpeg;base64,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Js2V6dVfLZZrX1lquKvUbNQq46hNwidnIVemt09Gz/aOce0rOPaOcf1P71v/xAArEAACAAMFCAMBAQEAAAAAAAABEQAQISAxUFFxQWGBkaHB8PFAseEwgNH/2gAIAQEAAT8h/wBrgg9BC6M3zGwOzghWqACgLrh3nwmwXcqA4B2eHP0IgrUhn7seIQUCoBwww+8QcaQMVcHkFgByuIRgxII8rJwxtBh/QF2qTpmPhvwxoBgp0fZmP8mRNQD9jDB2C7GYrXQZ6h2JqS30dCD3wxxi5T4ZzQH1CABd5+fT8MM88kqYg2/7/CirVfZHkneNgkjgOuTwxuhEFOpDP3IZMrp4hmpeanDiBrwDxKgYK4PIJVoVFxDuw9/BhnQFzQAaqtwZ7DD6aMEOj7M6VN5g0AHfD3QLsZjcgnmf8kEFu4FTPvd1lInhThFwnwzm2g0T4B3csjVc2Zcx0wrxzSpqrUESbyQMEjMHLyjKd8KfIRBTqQz9yrAumiCGO+pxnvulawDyrhJAV4B4lQANcPkEkMUVdaO9jUjqSZe0EJUOynz0ngNklw/gQQQQQQQWAwAyTA1Aw7oC+0/NINgdvHzE9xK6w5LIAj2WPZY9lj2WPZY9lj2WPfY3sCR8Wk3/AED+AdwARg+2UiNH3CaATfQ0H7Y1qE3ADmEahjDOcM5wznDOcM5wznDOccYUxt+Q+LQC5E7v0/jcKFzy5TVp2zw3WEeSd5+CaMcK9z+LsmfV+fFF0fHAvW0mG666awxyAUQFTWdPiFDqCaS6AervY4SOdJ8a9yPJNCbczENI9aj06PRo9Gj0aFroQHyygSgY4kuotLosLaNCxu1T1huo2yU5cxpAeYyaG1PSG6nbgLuue4ld7ITVxeQQ/wDbc1bBujfSOkljLpVjcaOkvAB0wI17ADwrAA1w+YWCiCiCNSF3jdZ0gPIZCusowKBSd5JgYECVyECdjrTSpO840IPa1vk+os6xw0cK9iz4Ns4a5z4s8IujDXLPrUs+XJ4bu8T1jSbL2hglm21w7cwHpOsG0OdMPAAgEao98j3KCcImG8/7W//aAAwDAQACAAMAAAAQ9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999983y99999999999999999999994861999999999999999999999W8sV999999999999999999999978/wDffffffffffffffffffffd++vvfffffffffffffffffffeddPfffffffffffffffffffffePPvfffffffffffffffffffffavNqVPfffffffffffffffffffaOHPAvffffffffffffffeffffb/ve12vvvutvffffffffa/PPLFLPawocsssnfffffffffbPjzPPfveAiF/TTf/fffffffffffeNPLffaQw/ffffffffffffffffX73ffQggPfffffffffffffffffffffSAivffffffffffffffffffffffgpPfffffffffffffffffffffbvv/fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff/xAAqEQEAAQIEBAYCAwAAAAAAAAABEQAQIUBRYXGRobEgMDFBYNHB8IHh8f/aAAgBAwEBPxD5c7grYoCUy4xtjKMucFuIUyximE42MLLGBUQca3KmOWCAKeAy4kllOXGRZSqLAie9AUB+sqMbZZZrnkrj4d8jLSpaVLSpaUcFpw22K6J9fmhhkox1Vvlb5W+VvlAEj5RkeGYN6cK0c2nljblw/Hh42l6+UzksblLAtgilhLb4iW5cd2glgoix6mv3LX7loz6J5qhG7xC+ya96cHevQK4qHfJQe9blOzdDf55luDpemXhNR92n0x3f6y/XTtaPUocv9y6D61DSgD0+Xf/EAB8RAQACAwACAwEAAAAAAAAAAAEAERAxQCAhMGBhUP/aAAgBAgEBPxD7cFy0tz74df0OkXG3NpHKTbmOibxtz7Ydx3RFAeXfJ0x0Oa6wMRsuWSyWSz49vEeppg28OzxNH4hqWloK864FiYdGf85+cACjjikS9IbHFaWi3kU8GzzjA+zznTg+l6K+3//EACsQAQABAQQLAAIDAQAAAAAAAAERABAhMcEgQVBRYXGBkaGx8EDRMIDx4f/aAAgBAQABPxD+68H9UNEowxlMKZrj50sd0nH99SvK/ZV3YJgHEF1gddnM8R1LQkDJcNp7s0mCXAvpY8U7valoAiTAnFgpymsHZnmTSQPdEcAcNQBloBfLg4N1SIgDdCy2YV3icainsUYaDhS3ABowADZi6AdckHs2zEJhLXQ3Amt6GQ2YeLjI1ztqQo33YQrv3rXEgbyEzwtmKQ9NJE72wdg/vwFO/lRhYg5cz6mzKuEdaszcUnklHiIeqGaorkMxfHPYPfIQwDfSjcWpstYJcC+nixXu9qVkBhIbpWsYz3hvdnSE3AbwHugRAGGoAysxaEbjUXHZxXWP8AnxRhZcoK96R87PJEgy5IPZtEvjv2APK2eeLjuM7aituYOKPRs1n94uJuK/21f7anQyFOGYxspe3Mkid7d4w/AX47rExMAeRYfdRF1kSF77wZHrZTPEWdnCiAlyMkHgsYZi9eTNCTgXcTZdN+82SLBLgU8eP93tSsNqCS3SuVYqa8xS+7EkTfV98rHnENl18sU43HrZPlFIAe6NkBYagDKx78YeQfNLi4wtiqysdEnhLDPSQvMSlNxlLmXfnonBZiLlgTF5fxr7PKvs8q+zyr7PKvs8q+zyr7PKmQ+AAAlW6ikDZ5g0MLGNYureC0C+v9A/VgwjuZq46PcKPv2ClehX0WVfRZV9FlX0WVfRZV9FlX0WVfXZVf8AsiSJ3S/izngZ5mTUVFRUVFRUUFivLeJDQdQLsEh2bR+3IRg93oQMcG5ij7tuAQI+hPmamtSe4sB7a4jvXEd64jvXEd64jvXEd64jvUu93p5tiCdSPt/FmyLvoC+3/CC0BN24gudBaeNkHFctDfNdE8bsjbcNABzUMypo+AXmuT+GBnGjmA9vxZlDSwyAL1wBb5Z8hnXyGdfIZ0D0gUUBinH0bXQDegzGVsRy6UFeXoXnwIbwlmtmh4JeYZKmQhTqAZthehhWAJqjYYmwM15aHTTSAaAQpErhxfy+qAylDsaLRTYh8D8AaDCsMnyDQDqrxybIIL+RCI5VAYhR4yJ4iwsKN9FUt4vPPYJvo6AFUMNCF6TzxHKlQKszxObQEo3lXkT6xY4RLE6jJQEEesWXlQqHUZtheaiBA9U5Ii01gOehIoU8g8ioAhgXaMxWVHqB4izG+nKSgAMAgsiFv6SSvo2EkiOugNIwwKSLpYslIr5bGGAfwIkKDdfc5OlMjL0ADk6MUnETkBns2KXiE6uiiZuk5Kfo2bJjd1oRM9HEMkfoJ8zs28mPUObQCUN7V5syPIy2a4OPbxSirgcLTbQKvIWlTEUubfs1kFLnVRhpHehZJvO9FHhi36/+mzxgYQAAea+6zr57Ony5iKn91v/Z" ,
            }
                

        self.generator = CaptchaGenerator()

    def get(self):
        """
        Generate a new captcha text
        """
        captcha_id = str(uuid4())

        # Slow generation in case of attack
        time.sleep(WAIT_TIME)

        img_array, answer = self.generator.generate_captcha()
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
