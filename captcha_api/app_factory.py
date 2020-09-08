from celery import Celery
from flask import Blueprint, Flask, redirect
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from captcha_api.database import db
from captcha_api.log_utils import configure_logging
from captcha_api.rest import api

index_bp = Blueprint('index', __name__)

celery = Celery()


@index_bp.route("/")
def index():
    return redirect("/swagger-ui")


def read_env_config(app: Flask):
    try:
        app.config.from_envvar("CAPTCHA_API_CONFIG")
    except Exception as e:
        app.logger.error(e)


def setup_api(app: Flask):
    api.version = app.config['API_VERSION']
    api.prefix = f"/api/{api.version}"
    api.init_app(app)


def make_celery(app):
    """
    Sets up Celery as a background task runner for the application
    """
    if app.config.get('USE_CELERY', False):
        celery.conf.broker_url = app.config['CELERY_BROKER_URL']
        celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
        celery.conf.update(app.config)

        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery.Task = ContextTask
    else:
        app.logger.warn('Celery is disabled!')


def create_app() -> Flask:
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CORS(app)
    app.url_map.strict_slashes = False
    app.config.from_object("captcha_api.config")
    app.logger = configure_logging()
    read_env_config(app)

    # Create a Celery connection
    make_celery(app)

    # DB initialization
    with app.app_context():
        db.init_app(app)
        db.create_all()

    setup_api(app)

    # Blueprints
    app.register_blueprint(index_bp)

    return app
