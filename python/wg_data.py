"""
special for https://github.com/OpenWGPAPI

>>> import papi
>>> api = Accounts(papi.Session(papi.Server.RU, 'demo'))

>>> api.getAccountID('Serb')
'461'
"""

import urllib

class Accounts(object):

    def __init__(self, api):
        self.api = api

    def getAccountList(self, params = {}):
        """getAccountList(params)\nMethod returns partial list of players. The list is filtered by initial characters of user name and sorted alphabetically."""
        return self.api.fetch('wot/account/list', urllib.urlencode(params))

    def getAccountInfo(self, params = {}):
        """getAccountInfo(params)\nMethod returns player details."""
        return self.api.fetch('wot/account/info', urllib.urlencode(params))

    def getAccountTanks(self, params = {}):
        """getAccountTanks(params)\nMethod returns details on player's vehicles."""
        return self.api.fetch('wot/account/tanks', urllib.urlencode(params))

    def getAccountAchievements(self, params = {}):
        """getAccountAchievements(params)\nThis method returns players' achievement details."""
        return self.api.fetch('wot/account/achievements', urllib.urlencode(params))

    def getAccountID(self, name):
        """getAccountID(name)\nMethod returns account ID by name."""
        page = self.getAccountList({'search': name, 'fields': 'account_id', 'limit': '1'})

        if page:
            return str(page[0]['account_id'])
        return None

if __name__ == "__main__":
    import doctest
    doctest.testmod()
