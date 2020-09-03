import os
from lirc import RawConnection
from MappingHelper import loadMap, getMappingFromDB

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

class SignalHandler():
    def __init__(self, thread_list):
        self.SIGINT = False
        self.thread_list = thread_list

    def terminate(self, signal, frame):
        print('[i] Exiting!')
        self.SIGINT = True
    
    def update(self, signal, frame):
        print("[i] Refreshing mapping...")
        for thread in self.thread_list:
            thread.updateMapping()

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

if __name__ == "__main__":
    PID = os.getpid()
        print("[i] Starting hklirc with pid= "+str(PID))
        with open(PID_PATH, "w") as f:
            f.write(str(PID))

    # Loading standard Keymap
    KEY_MAP = loadMap(self.map)
    # Reading user mapping from DB
    #self.updateMapping()

    # Init IR connection
    conn = RawConnection()
    #print("[i] Starting Up...")
    handler = SignalHandler([irThread])
    signal.signal(signal.SIGINT, handler.terminate)
    signal.signal(signal.SIGTERM, handler.terminate)
    signal.signal(signal.SIGUSR1, handler.update)

    while not handler.SIGINT:
        command = self.getIrCommand(conn)
        
        # We override with the usermapping command
        if (command in self.user_mapping):
                command = self.user_mapping[command]
        
        # We trigger the proper KEY
        if (command is not None) and (command in KEY_MAP): 
            currentMap = KEY_MAP[command]
            print(currentMap)
            if (currentMap['keyboard']):
                sendKey(int(currentMap['value'],0))
            else:
                sendMultimediaKey(int(currentMap['value'],0))