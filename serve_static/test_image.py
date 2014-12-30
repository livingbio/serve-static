import os
import unittest
from google.appengine.ext import testbed

class CacheImageTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_all_stubs()

    def test_cache_image(self):
        from image import cache_image
        x = cache_image('test-bucket', "http://www.tagtoo.com.tw/static/website/img/member/Master.jpg")

