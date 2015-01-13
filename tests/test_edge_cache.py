# -*- encoding=utf8 -*-
from mock import patch, MagicMock
import unittest
import webtest
from google.appengine.ext import testbed
from datetime import datetime, timedelta
import re
import webapp2
from serve_static.edge_cache import expires

class TestExpire(unittest.TestCase):
    def _createApp(self, url, handler):
        return webtest.TestApp(webapp2.WSGIApplication([(url, handler)], debug=True))

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_all_stubs()

    re_max_age = re.compile(r'public, max-age=([\d]+)')
    def assertCache(self, headers, except_max_age):
        self.assertTrue(self.re_max_age.match(headers['Cache-Control']))
        max_age = int(self.re_max_age.findall(headers['Cache-Control'])[0])
        self.assertTrue(except_max_age-10 < max_age < except_max_age+10)
        self.assertEqual(headers['Pragma'], 'Public')

    def test_expire_interval(self):
        class TestExpireInterval(webapp2.RequestHandler):
            @expires(expire_interval=timedelta(days=10))
            def get(self):
                pass

        except_max_age = 10 * 24 * 60 * 60
        app = self._createApp('/test', TestExpireInterval)
        resp = app.get('/test')
        self.assertCache(resp.headers, except_max_age)

    def test_force_expire(self):
        class TestForceExpire(webapp2.RequestHandler):
            @expires(force_expires=datetime.utcnow()+timedelta(days=10))
            def get(self):
                pass

        except_max_age = 10 * 24 * 60 * 60
        app = self._createApp('/test', TestForceExpire)
        resp = app.get('/test')
        self.assertCache(resp.headers, except_max_age)

    def test_force_expire_too_long(self):
        class TestForceExpireTooLong(webapp2.RequestHandler):
            @expires(force_expires=datetime.utcnow()+timedelta(days=3000))
            def get(self):
                pass

        except_max_age = 364 * 24 * 60 * 60
        app = self._createApp('/test', TestForceExpireTooLong)
        resp = app.get('/test')
        self.assertCache(resp.headers, except_max_age)

    def test_no_expires(self):
        class TestNoExpire(webapp2.RequestHandler):
            @expires()
            def get(self):
                pass

        app = self._createApp('/test', TestNoExpire)
        resp = app.get('/test')
        self.assertEqual(resp.headers['Cache-Control'], 'no-cache')
        self.assertNotEqual(resp.headers.get('Pragma'), 'Public')

    def test_no_cache(self):
        class TestNoCache(webapp2.RequestHandler):
            @expires(force_expires=datetime.utcnow()+timedelta(days=10))
            def get(self):
                self.response.headers['no-cache'] = 'true'

        app = self._createApp('/test', TestNoCache)
        resp = app.get('/test')
        self.assertEqual(resp.headers['Cache-Control'], 'no-cache')
        self.assertNotEqual(resp.headers.get('Pragma'), 'Public')

