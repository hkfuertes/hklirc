import os, signal
from lirc import RawConnection
from MappingHelper import loadMap, getMappingFromDB

PID_PATH = "../DAEMON_PID"
MAP_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),"../standard_map.json"))
DB_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),"../hklirc.db"))

############################################################################## HID HELPERS ##
# Descriptor:
#   05010906a1018501050719e029e71500250175019508810295017508810395057501050819012905910295017
#   503910395067508150025650507190029658100c0050C0901A1018502050C150025017501950709B509B609B7
#   09CD09E209E909EA810295068101C0

KEYBOARD_ID = chr(0x01)
CONSUMER_ID = chr(0x02)
NULL_CHAR = chr(0)

def write_report(report, file = '/dev/hidg0' ):
    with open(file, 'rb+') as fd:
        fd.write(report.encode())

def sendKey(key, file = '/dev/hidg0'):
    write_report(KEYBOARD_ID+NULL_CHAR*2+chr(key)+NULL_CHAR*5, file)
    write_report(KEYBOARD_ID+NULL_CHAR*8, file)

def sendMultimediaKey(key, file = '/dev/hidg0'):
    write_report(CONSUMER_ID+chr(key)+NULL_CHAR, file)
    write_report(CONSUMER_ID+NULL_CHAR*2, file)
#############################################################################################

class hklircd():
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    map = None
    db = None
    user_mapping = {}
    stopped = False

    def __init__(self, map, db):
        self.map = map
        self.db = db
    
    def updateMapping(self):
        self.user_mapping = getMappingFromDB(self.db)

    def getIrCommand(self, conn):
        try:
            keypress = conn.readline(.0001)
        except:
            keypress=""
                
        if (keypress != "" and keypress != None):
                    
            data = keypress.split()
            sequence = data[1]
            command = data[2]
            
            #ignore command repeats
            if (sequence != "00"):
                return
            
            return command

    def run(self):
        if ((self.map is None) or (self.db is None)):
            return

        print("[i] Starting Lirc Listener...")

        # Loading standard Keymap
        KEY_MAP = loadMap(self.map)
        # Reading user mapping from DB
        self.updateMapping()

        # Init IR connection
        conn = RawConnection()

        while True:
            command = self.getIrCommand(conn)
            if (command is not None):
                print(command)
                if (command in self.user_mapping):
                    command = self.user_mapping[command]
            
                # We trigger the proper KEY
                if (command in KEY_MAP): 
                    currentMap = KEY_MAP[command]
                    print(currentMap)
                    if (currentMap['keyboard']):
                        sendKey(int(currentMap['value'],0))
                    else:
                        sendMultimediaKey(int(currentMap['value'],0))

if __name__ == "__main__":
    PID = os.getpid()
    print("[i] Starting hklirc with pid = "+str(PID))
    with open(PID_PATH, "w+") as f:
        f.write(str(PID))
    
    print(MAP_FILE); print(DB_FILE)

    server = hklircd(map=MAP_FILE, db=DB_FILE)

    print(getMappingFromDB(DB_FILE))

    # Prepare to receive SIGUSR1
    signal.signal(signal.SIGUSR1, server.updateMapping)

    # Run!
    try:
        server.run()
    except KeyboardInterrupt:
        print("[i] Exiting!")

    os.remove(PID_PATH)
