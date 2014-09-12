import json, logging, time

import web

class Error(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class Request(object):

    def __init__(self, api_host, api_key):
        self.api_host = api_host
        self.api_key = api_key

    def fetch(self, url, params):
        page = web.Page("http://api.%s/%s/?application_id=%s&%s" % (self.api_host, url, self.api_key, params))
        count = 0
        while count < 5:
            resp = json.loads(page.fetch())
            if resp['status'] == 'ok':
                return resp['data']
            count += 1
            logging.info("### PAPI retry %d %s" % (count, page.url))
            time.sleep(5)

        raise Error(repr(resp))
