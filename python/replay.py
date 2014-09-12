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

class File(object):

    def __init__(self, input_file):
  
        sign, block_count = struct.unpack('ll', input_file.read(8))
        self.sign = sign
        self.json_battle_initial = None
        self.json_battle_result = None
      
        if self.sign == SIGN.REGULAR:
            pass
        elif self.sign == SIGN.COMP2:
            raise Exception("It's wotreplay file, but this format is unknown")
        else:
            raise Exception("Looks like not wotreplay file, sign: %d" % self.sign)
      
        block_len, = struct.unpack('l', input_file.read(4))
        self.json_battle_initial = json.loads(input_file.read(block_len))
      
        if block_count > 1:
            block_len, = struct.unpack('l', input_file.read(4))
            self.json_battle_result = json.loads(input_file.read(block_len))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:

        try:

            rep = File(open(sys.argv[1], 'rb'))
            if rep.json_battle_result:
                print "Record completed"
            else:
                print "Record NOT completed"
            if (len(sys.argv) > 2) and sys.argv[2] == 'dump':
                print "\nInitial battle data:\n"
                print json.dumps(rep.json_battle_initial, indent=2)
                if rep.json_battle_result:
                    print "\nResult battle data:\n"
                    print json.dumps(rep.json_battle_result, indent=2)

        except Exception, e:
            print "Error: %s" % e
    else:
        print "Usage:\npython replay.py filename.wotreplay [dump]"
