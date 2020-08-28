import signal, os
from LircThread import LircThread
from WiimoteThread import WiimoteThread

PID_PATH = "../DAEMON_PID"

class SignalHandler():
    def __init__(self, thread_list):
        self.SIGINT = False
        self.thread_list = thread_list

    def terminate(self, signal, frame):
        print('[i] Exiting!')
        for thread in self.thread_list:
            thread.stop()
        self.SIGINT = True
    
    def update(self, signal, frame):
        print("[i] Refreshing mapping...")
        for thread in self.thread_list:
            thread.updateMapping()


if __name__ == "__main__":
    PID = os.getpid()
    print("[i] Starting hklirc with pid= "+str(PID))
    with open(PID_PATH, "w") as f:
        f.write(str(PID))
    
    irThread = LircThread()
    wiiThread = WiimoteThread()

    # Prepare to receive SIGINT, SIGTERM, SIGUSR1
    handler = SignalHandler([irThread, wiiThread])
    signal.signal(signal.SIGINT, handler.terminate)
    signal.signal(signal.SIGTERM, handler.terminate)
    signal.signal(signal.SIGUSR1, handler.update)

    irThread.config(map="../standard_map.json", db="../hklirc.db")
    irThread.start()

    wiiThread.config(map="../standard_map.json", db="../hklirc.db")
    wiiThread.start()

    while not handler.SIGINT:
        continue
    
    os.remove(PID_PATH)