from datetime import datetime, timedelta

from .app import celery
from .db import db
from .models import Captcha


@celery.task
def delete_old_captchas():
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    old_captchas = Captcha.query.filter(Captcha.creation_time <= one_hour_ago)
    old_captchas.delete()
    db.session.commit()
