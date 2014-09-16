import papi

nick_name = 'Serb'

try:
    data = papi.Session(papi.Server.RU, 'demo').fetch('wot/account/list', 'search=%s&limit=1' % nick_name)
    print "Hi, %s! I know your ID on RU server: %s" % (nick_name, data[0]['account_id'])

except papi.Error as e:
    print "WG PAPI error: %s" % e

except Exception as e:
    print "Error: %s" % e
