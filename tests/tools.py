import json
import os
import unittest
from abc import ABCMeta
from unittest.mock import MagicMock, patch

from flask import Flask
from flask.testing import FlaskClient

from captcha_api.app_factory import create_app

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

    def _create_app(self):
        self.app = create_app()
        self.app.testing = True
        self.app_client = self.app.test_client()

    def setUp(self):
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, {"CAPTCHA_API_CONFIG": "tests/testing_config.py"}).start()
        self._create_app()
