from ogn.client import AprsClient
from ogn.parser import parse, ParseError
from datetime import datetime

class self():
    def __init__():
        self.max = 10 * 1000000  #given in seconds and converted to microseconds
        self.average = [0,0,0,0] #dif[0], dif[1], dif[2], count

def timekeeping(beacon):
    try:
        ori = beacon["timestamp"]                                        #original
        ref = beacon["reference_timestamp"]                              #reference
        act = datetime.now()                                             #actual
        dif = [ref - ori, act - ori, act - ref]                          #plane-server, plane-pi, server-pi

        i = -1
        for item in dif:
            i += 1
            nums = str(item).split(":")
            microsec = int(nums[0]) * 3600000000                         #microsec =  h  * 3.6 * 10^9
            microsec += int(nums[1]) * 60000000                          #microsec = min *  6  * 10^7
            microsec += int(nums[2].split(".")[0]) * 1000000             #microsec =  s  *  1  * 10^6
            dif[i] = microsec + int(nums[2].split(".")[1])

            #average bulding function

        self.average[3] += 1
        if dif[1] > self.max: return False
        return True

    except:
        return None

def process_beacon(raw_message):
    try:
        beacon = parse(raw_message)
    except:
        return

    if beacon["aprs_type"] == "position" and beacon["beacon_type"] == "flarm" and beacon["aircraft_type"] == 1:
        allowed = timekeeping(beacon)

#                print("plane - server ", dif1, " plane - pi ", dif2, " server - pi ", dif3)
#                return

#        print("\033[31mplane - server ", dif1, " plane - pi ", dif2, " server - pi ", dif3, "\033[39m")
#        return

    return

client = AprsClient(aprs_user='N0CALL')
client.connect()

try:
    client.run(callback=process_beacon, autoreconnect=True)
except KeyboardInterrupt:
    print('\nStop ogn gateway')
    client.disconnect()
