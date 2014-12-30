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
        import urllib
        url1 = cache_image('test-bucket', "http://www.tagtoo.com.tw/static/website/img/member/Master.jpg")
        url2 = cache_image('test-bucket', 'http://www.tagtoo.com.tw/static/website/img/member/Master.jpg', urllib.urlopen('http://www.tagtoo.com.tw/static/website/img/member/Master.jpg'))
        self.assertEqual(url1, url2)
        
