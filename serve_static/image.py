import cloudstorage as gcs
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.api import urlfetch
import logging
import hashlib

def create_gs_file(bucket, filename, content):
    with gcs.open("/%s/%s"%(bucket, filename), 'w') as f:
        f.write(content)

    return True


def exist_gs_file(bucket, filename):
    try:
        gcs.stat("/%s/%s"%(bucket, filename))
        return True
    except gcs.NotFoundError:
        return False

def filehash(content):
    m = hashlib.md5()
    m.update(content)
    return m.hexdigest()

def cache_image(bucket, url, content=None):
    if not content:
        content = urlfetch.fetch(url, headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}).content

    filename = filehash(content)
    if exist_gs_file(bucket, filename):
        blob_key = blobstore.create_gs_key("/gs/%s/%s" % (bucket, filename))
    else:
        create_gs_file(bucket, filename, content)
        blob_key = blobstore.create_gs_key("/gs/%s/%s" % (bucket, filename))

    return images.get_serving_url(blob_key)

