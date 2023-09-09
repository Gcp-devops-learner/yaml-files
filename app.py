# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = "SriCharanK"

import time
import redis
from flask import Flask
import os

app = Flask(__name__)
cache = redis.Redis(host=os.getenv('REDIS_SERVER'), port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hit():
    count = get_hit_count()
    return 'Hello, you have %i visitors on this page' % int(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
