import threading, time, cwiid
from Helpers.MappingHelper import loadMap, getMappingFromDB
from Helpers.HidHelper import sendKey, sendMultimediaKey


class WiimoteThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    map = None
    db = None
    user_mapping = {}

    def __init__(self):
        super(WiimoteThread, self).__init__()
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
        super(WiimoteThread,self).join(*args, **kwargs)

    def convertWiiButton(self, buttons):
        if (buttons & cwiid.BTN_LEFT):
            return "KEY_LEFT"

        if(buttons & cwiid.BTN_RIGHT):
            return "KEY_RIGHT"

        if (buttons & cwiid.BTN_UP):
            return "KEY_UP"
        
        if (buttons & cwiid.BTN_DOWN):
            return "KEY_DOWN"
        
        if (buttons & cwiid.BTN_1):
            return "KEY_1"

        if (buttons & cwiid.BTN_2):
            return "KEY_2"

        if (buttons & cwiid.BTN_A):
            return "KEY_A"

        if (buttons & cwiid.BTN_B):
            return "KEY_B"

        if (buttons & cwiid.BTN_HOME):
            return "KEY_HOME"
        
        if (buttons & cwiid.BTN_MINUS):
            return "KEY_VOLUMEDOWN"
        
        if (buttons & cwiid.BTN_PLUS):
            return "KEY_VOLUMEUP"

    def run(self):
        while not self._stop_event.is_set():
            self.runSingleLoop()

    def runSingleLoop(self):
        if ((self.map is None) or (self.db is None)):
            return

        print("[i] Starting Wiimote Listener...")

        # Loading standard Keymap
        KEY_MAP = loadMap(self.map)
        # Reading user mapping from DB
        self.updateMapping()

        button_delay = 0.2
        try:
            wii=cwiid.Wiimote()
        except RuntimeError:
            print ("[!] Error opening wiimote connection")
            return

        wii.rpt_mode = cwiid.RPT_BTN

        # Rumble to say we are connected
        wii.rumble = 1
        time.sleep(.4)
        wii.rumble = 0

        wii.led = 1
        #print("[i] Starting Up...")
        while not self._stop_event.is_set():
            buttons = wii.state['buttons']

            if (buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):  
                print ('[!] Closing connection ...')
                return

            command = self.convertWiiButton(buttons)
            if (command is not None) and (command in KEY_MAP): 
                currentMap = KEY_MAP[command]
                if (command in self.user_mapping):
                    currentMap = KEY_MAP[self.user_mapping[command]]
                print(currentMap)
                if (currentMap['keyboard']):
                    sendKey(int(currentMap['value'],0))
                else:
                    sendMultimediaKey(int(currentMap['value'],0))
            time.sleep(button_delay)
