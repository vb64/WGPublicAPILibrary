"""
Example of python class for using Wargaming PublicAPI
(C) 2014 by Vitaly Bogomolov mail@vitaly-bogomolov.ru
special for https://github.com/OpenWGPAPI

based on: https://ru.wargaming.net/support/Knowledgebase/Article/View/713/25/primer-prkticheskogo-ispolzovnija-metodov-api-c-pltformnet

>>> import papi
>>> api = papi.Session(papi.Server.RU, 'demo')
>>> api.fetch('wot/account/list', 'search=%s&limit=1' % 'Serb')
[{u'nickname': u'SerB', u'id': None, u'account_id': 461}]
>>> api.isClanDeleted(90)
True
>>> api.isClanDeleted(1)
False
>>> api.getPlayerID('sss___sss__Serb')

>>> api.getPlayerID('Serb')
'461'
"""

import urllib2, json, logging, time

NUM_RETRIES = 5
DELAY_SECONDS = 5

class Server:
  RU   = 'worldoftanks.ru'
  EU   = 'worldoftanks.eu'
  COM  = 'worldoftanks.com'
  SEA  = 'worldoftanks.asia'
  KR   = 'worldoftanks.kr'
  
class Error(Exception):
    pass

class Page(object):

    def __init__(self, url):

        self.url = url
        self.row_text = ''
        self.response_code = 0
        self.response_info = ()

        # uncomment for deploy at GoogleAppEngine platform
        # this supress GAE fucking cash using
        #
        #import random
        #
        #delim = '?'
        #if delim in url:
        #    delim = '&'
        #self.url = "%s%s%s" % (url, delim, str(random.random()))  
  
    def fetch(self):
  
        last_exception = None
        count = 0
        is_ok = False
      
        while (not is_ok) and (count < NUM_RETRIES):
      
            try:
                response = urllib2.urlopen(self.url, None, 30)
                is_ok = True
            except Exception as e:
                last_exception = e
                count += 1
                time.sleep(DELAY_SECONDS)
      
        if not is_ok:
            raise last_exception
      
        if response.getcode() > 200:
            raise Error("urlopen code: %d url: %s" % (response.getcode(), self.url))
      
        self.response_code = response.getcode()
        self.response_info = response.info()
        self.row_text = response.read()
        return self.row_text

class Session(object):

    def __init__(self, api_host, api_key):
        self.api_host = api_host
        self.api_key = api_key

    def fetch(self, url, params):
        page = Page("http://api.%s/%s/?application_id=%s&%s" % (self.api_host, url, self.api_key, params))
        count = 0
        while count < NUM_RETRIES:
            resp = json.loads(page.fetch())
            if resp['status'] == 'ok':
                return resp['data']
            count += 1
            logging.info("### PAPI retry %d %s" % (count, page.url))
            time.sleep(DELAY_SECONDS)

        raise Error(repr(resp))

    # trick for check for deleted clan
    def isClanDeleted(self, clan_id):
        page = Page("http://api.%s/%s/?application_id=%s&%s" % (self.api_host, 'wot/clan/provinces', self.api_key, 'clan_id=%d' % clan_id))
        count = 0

        while count < NUM_RETRIES:

            r = json.loads(page.fetch())
            if r['status'] == 'ok':
                return False
            elif (r['status'] == 'error') and (r['error']['code'] == 404) and (r['error']['message'] == 'CLAN_NOT_FOUND'):
                return True

            count += 1
            logging.info("### PAPI retry %d %s" % (count, page.url))
            time.sleep(DELAY_SECONDS)

        return False
    
    def getPlayerID(self, name):
        """getPlayerID(name)\nReturn player ID by name"""
        page = self.fetch('wot/account/list', 'search=%s&fields=account_id&limit=1' % name)

        if page:
            return str(page[0]['account_id'])
        return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
