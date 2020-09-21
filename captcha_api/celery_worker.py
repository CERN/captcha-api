from celery.schedules import crontab

from .app import celery, create_app
from .tasks import delete_old_captchas


app = create_app()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every hour the delete old captchas task
    sender.add_periodic_task(
        crontab(minute=0, hour="*/1"),
        delete_old_captchas.s(),
    )
