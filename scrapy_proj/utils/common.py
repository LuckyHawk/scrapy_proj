# -*- coding: utf-8 -*-

import hashlib

def get_md5(url):
    url = url.encode('utf-8') if isinstance(url,unicode) else url
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()