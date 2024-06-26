import os
import tempfile
from HTTPSocket import HTTPSocket

class ComputerCMD:
    def __init__(self, panelURL, machineID):
        self.C = HTTPSocket(str(panelURL), str(machineID))
        self.tempdir = tempfile.gettempdir()

    def shutdown(self):
        try:
            cmd = "shutdown -s -t 00"
            self.C.Log("Succ", "Shutdown Command Executed Successfully")
            self.C.Send("CleanCommands")
            os.system(cmd)
        except Exception as e:
            self.C.Send("CleanCommands")
            print("[Error In ComputerCMD, shutdown() Function]")
            print(f"[Error] : {e}")
            self.C.Log("Fail", "An unexpected error ocurred" + str(e))

    def restart(self):
        try:
            cmd = "shutdown -r -t 00"
            self.C.Log("Succ", "Shutdown Command Executed Successfully")
            self.C.Send("CleanCommands")
            os.system(cmd)
        except Exception as e:
            self.C.Send("CleanCommands")
            print("[Error In ComputerCMD, restart() Function]")
            print(f"[Error] : {e}")
            self.C.Log("Fail", "An unexpected error ocurred" + str(e))


    def logoff(self):
        try:
            cmd = "shutdown -l"
            self.C.Log("Succ", "LogOff Command Executed Successfully")
            self.C.Send("CleanCommands")
            os.system(cmd)
        except Exception as e:
            self.C.Send("CleanCommands")
            print("[Error] In ComputerCMD, logoff() Function]")
            print(f"[Error]:{e}")
            self.C.Log("Fail", "An unexpected error occured" + str(e))
