import datetime
import json
import unittest
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

from captcha_api.database import Captcha, db
from tests.tools import API_ROOT, WebTestBase


class TestCaptchaApi(WebTestBase):

    CAPTCHA_ROOT = f"{API_ROOT}/captcha"

    def test_create_captcha(self):
        resp = self.app_client.get(self.CAPTCHA_ROOT)

        self.assertIsNotNone(UUID(resp.json['id']))
        self.assertIsNotNone(resp.json['img'])
        self.assertEqual(200, resp.status_code)

        with self.app.app_context():
            db_captcha = Captcha.query.get(resp.json['id'])
            self.assertIsNotNone(db_captcha)
            self.assertIsNotNone(db_captcha.answer)
            self.assertIsNotNone(db_captcha.creation_time)

    def test_answer_missing_captcha(self):
        resp = self.app_client.get(self.CAPTCHA_ROOT)

        self.assertIsNotNone(UUID(resp.json['id']))
        self.assertEqual(200, resp.status_code)

        answer_res = self.app_client.post(self.CAPTCHA_ROOT,
                                          data=json.dumps(
                                              {"id": str(uuid4()), 'answer': '42'}),
                                          content_type='application/json'
                                          )
        self.assertEqual(404, answer_res.status_code)

    def test_create_captcha_and_answer_wrong(self):
        resp = self.app_client.get(self.CAPTCHA_ROOT)

        self.assertIsNotNone(UUID(resp.json['id']))
        self.assertEqual(200, resp.status_code)

        answer_res = self.app_client.post(self.CAPTCHA_ROOT,
                                          data=json.dumps(
                                              {"id": resp.json['id'], 'answer': '42'}),
                                          content_type='application/json'
                                          )
        self.assertEqual(400, answer_res.status_code)
        self.assertTrue(
            "invalid answer" in answer_res.json['message'].casefold())

    def test_create_captcha_and_answer_uppercase_works_and_removes_it(self):
        resp = self.app_client.get(self.CAPTCHA_ROOT)

        self.assertIsNotNone(UUID(resp.json['id']))
        self.assertEqual(200, resp.status_code)

        with self.app.app_context():
            db_captcha = Captcha.query.get(resp.json['id'])
            answer_res = self.app_client.post(self.CAPTCHA_ROOT,
                                              data=json.dumps(
                                                  {"id": resp.json['id'], 'answer': db_captcha.answer.upper()}),
                                              content_type='application/json'
                                              )
            self.assertEqual(200, answer_res.status_code)

    def test_create_captcha_and_answer_right_works_and_removes_it(self):
        resp = self.app_client.get(self.CAPTCHA_ROOT)

        self.assertIsNotNone(UUID(resp.json['id']))
        self.assertEqual(200, resp.status_code)

        with self.app.app_context():
            db_captcha = Captcha.query.get(resp.json['id'])
            answer_res = self.app_client.post(self.CAPTCHA_ROOT,
                                              data=json.dumps(
                                                  {"id": resp.json['id'], 'answer': db_captcha.answer}),
                                              content_type='application/json'
                                              )
            self.assertEqual(200, answer_res.status_code)

            answer_res = self.app_client.post(self.CAPTCHA_ROOT,
                                              data=json.dumps(
                                                  {"id": resp.json['id'], 'answer': db_captcha.answer}),
                                              content_type='application/json'
                                              )
            self.assertEqual(404, answer_res.status_code)

    def test_create_captcha_and_answer_too_late_does_not_work(self):
        resp = self.app_client.get(self.CAPTCHA_ROOT)

        self.assertIsNotNone(UUID(resp.json['id']))
        self.assertEqual(200, resp.status_code)

        with self.app.app_context():
            db_captcha = Captcha.query.get(resp.json['id'])
            db_captcha.creation_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=2)
            db.session.commit()

            answer_res = self.app_client.post(self.CAPTCHA_ROOT,
                                              data=json.dumps(
                                                  {"id": resp.json['id'], 'answer': db_captcha.answer}),
                                              content_type='application/json'
                                              )
            self.assertEqual(400, answer_res.status_code)
            self.assertTrue(
                "did not answer fast enough" in answer_res.json['message'].casefold())
