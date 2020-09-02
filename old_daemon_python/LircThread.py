import threading, time
from lirc import RawConnection
from Helpers.MappingHelper import loadMap, getMappingFromDB
from Helpers.HidHelper import sendKey, sendMultimediaKey


class LircThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    map = None
    db = None
    user_mapping = {}

    def __init__(self):
        super(LircThread, self).__init__()
        self._stop_event = threading.Event()

    def config(self, map, db):
        self.map = map
        self.db = db
    
    def updateMapping(self):
        self.user_mapping = getMappingFromDB(self.db)

    def stop(self):
        self._stop_event.set()

    def join(self, *args, **kwargs):
        self.stop()
        super(LircThread,self).join(*args, **kwargs)

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
        #print("[i] Starting Up...")
        while not self._stop_event.is_set():
            command = self.getIrCommand(conn)
            if (command is not None) and (command in KEY_MAP): 
                currentMap = KEY_MAP[command]
                if (command in self.user_mapping):
                    currentMap = KEY_MAP[self.user_mapping[command]]
                print(currentMap)
                if (currentMap['keyboard']):
                    sendKey(int(currentMap['value'],0))
                else:
                    sendMultimediaKey(int(currentMap['value'],0))