import papi

print papi.Session(papi.Server.RU, 'demo').fetch('wot/account/list', 'search=%s&limit=1' % 'Serb')
