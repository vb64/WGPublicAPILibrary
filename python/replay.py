"""
Example of python class for decoding Wargaming .wotreplay file
(C) 2014 by Vitaly Bogomolov mail@vitaly-bogomolov.ru
special for https://github.com/OpenWGPAPI

Usage:
python replay.py filename.wotreplay [dump]

useful links:

http://wiki.vbaddict.net/pages/File_Replays
https://bitbucket.org/wotreplays/wot-replay-parser/wiki/Format/Basics
https://github.com/raszpl/wotdecoder

"""

import struct, json

class SIGN:
    REGULAR = 288633362
    COMP2   = 14

battleType = [
    "???", 
    "public", 
    "training", 
    "tankcompany", 
    "???", 
    "clanwar", 
    "???", 
    "742",
    "???", 
    "???", 
    "stronghold",
]

class File(object):

    def __init__(self, input_file):
        
        # read from wotreplay file 2 long values (4 + 4 = 8 bytes)
        # first long - file signature
        # second long - count of blocks with json data
        sign, block_count = struct.unpack('ll', input_file.read(8))
        
        self.sign = sign
        self.json_battle_initial = None
        self.json_battle_result = None
      
        # check for valid file signature
        if self.sign == SIGN.REGULAR:
            pass
        elif self.sign == SIGN.COMP2:
            raise Exception("It's wotreplay file, but this format is unknown")
        else:
            raise Exception("Looks like not wotreplay file, sign: %d" % self.sign)
      
        # read next long value (4 bytes). it's length in bytes for next json string.
        block_len, = struct.unpack('l', input_file.read(4))
        
        # read json string of a given size and convert to python data types
        # save as data at battle start
        self.json_battle_initial = json.loads(input_file.read(block_len))
      
        # if file contain block with json data at battle finish (complete record, player not leaves battle)
        if block_count > 1:
            
            # read long value (4 bytes) as size of next json string
            block_len, = struct.unpack('l', input_file.read(4))
            
            # read json string of a given size and convert to python data types
            # save as data at battle finish
            self.json_battle_result = json.loads(input_file.read(block_len))

class Data(File):

    def dump_json_data(self):

        ret = "\nInitial battle data:\n"
        ret = "%s%s" % (ret, json.dumps(self.json_battle_initial, indent=2))
        if self.json_battle_result:
            ret = "%s%s" % (ret, "\nResult battle data:\n")
            ret = "%s%s" % (ret, json.dumps(self.json_battle_result, indent=2))
        return ret

    def dump_common_info(self):

        j = self.json_battle_initial
        ret = "Version: %s\n" % j['clientVersionFromExe']
        ret = "%s%s" % (ret, "Date: %s\n" % j['dateTime'])
        ret = "%s%s" % (ret, "Map: %s\n" % j['mapName'])
        ret = "%s%s" % (ret, "Player: %s on tank '%s'\n" % (j['playerName'], j['playerVehicle']))

        b = 'unknown'
        if j['battleType'] < len(battleType):
            b = battleType[j['battleType']]

        ret = "%s%s" % (ret, "Battle: %s (%s)\n" % (b, j['gameplayID']))
        if not self.json_battle_result:
            ret = "%s%s" % (ret, "Record NOT completed\n")
            return ret

        j = self.json_battle_result
        ret = "%s%s" % (ret, "Winner Team: %s\n" % j[0]['common']['winnerTeam'])
        return ret

    def dump_teams(self):

        team1 = []
        team2 = []
        j = self.json_battle_initial

        for uid, data in j['vehicles'].items():
            lst = (data['name'], data['clanAbbrev'], data['vehicleType'])
            if data['team'] == 1:
                team1.append(lst)
            else:
                team2.append(lst)

        ret = ""
        for num, team in [(1, team1), (2, team2)]:
            ret = "%s%s" % (ret, "\nTeam%d (%d):\n\n" % (num, len(team)))
            for itm in team:
                cl = ""
                if itm[1]:
                    cl = " [%s]" % itm[1]
                ret = "%s%s" % (ret, "%s%s\n" % (itm[0], cl))

        return ret

def main():

    import sys

    if len(sys.argv) > 1:

        try:
            rep = Data(open(sys.argv[1], 'rb'))
        except Exception, e:
            print "Error: %s" % e
            return

        print rep.dump_common_info()
        print rep.dump_teams()

        if (len(sys.argv) > 2) and sys.argv[2] == 'dump':
            print rep.dump_json_data()

    else:
        print "Usage:\npython replay.py filename.wotreplay [dump]"

if __name__ == "__main__":
    main()
