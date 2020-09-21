import unittest
from abc import ABCMeta
from unittest.mock import patch

import flask_migrate
from flask import Flask
from flask.testing import FlaskClient

from captcha_api.app import create_app


API_ROOT = "/api/v1.0"


class WebTestBase(unittest.TestCase, metaclass=ABCMeta):
    """
    Base Class for web app tests
    """

    def __init__(self, name):
        super().__init__(name)
        self.app: Flask = None
        self.app_client: FlaskClient = None
        self.user_info_mock = None
        self.jwt_mock = None

    def _create_app(self, overrides):
        self.app = create_app(config_override=overrides, use_env_config=False)
        self.app.testing = True
        self.app_client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        flask_migrate.upgrade(revision="head")

    def setUp(self):
        self.addCleanup(patch.stopall)
        self._create_app({"SQLALCHEMY_DATABASE_URI": "sqlite://"})

    def tearDown(self):
        flask_migrate.downgrade()
        self.ctx.pop()
