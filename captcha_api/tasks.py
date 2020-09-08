from datetime import datetime, timedelta

from captcha_api.app_factory import celery
from captcha_api.database import Captcha, db


@celery.task
def delete_old_captchas():
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    old_captchas = Captcha.query.filter(
        Captcha.creation_time <= one_hour_ago)
    old_captchas.delete()
    db.session.commit()
