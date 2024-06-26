import os
import sys
import subprocess
import re
import uuid
import ctypes

class BypassVM:

    def registry_check(self):
        reg1 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\CONTROLSet001\\Control\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul")
        reg2 = os.system("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul")

        if reg1 != 1 and reg2 != 1:
            print("VMare Registry Detected")

    def process_and_files_check(self):
        vmware_dll = os.path.join(os.environ["SystemRoot"], "System32\\vmGuestLib.dll")
        virtualbox_dll = os.path.join(os.environ["SystemRoot"], "vboxmrxnp.dll")

        process = os.popen('TASKLIST /FI "STATUS eq RUNNING" | find /V "Image Name" | find /V "="').read()
        processList = []
        for processNames in process.split():
            if ".exe" in processNames:
                processList.append(processNames.replace("K\n", "").replace("\n", ""))

        if "VMwareService.exe" in processList or "VMwareTray.exe" in processList:
            print("VMwareService.exe & VMwareTray.exe process are running")
            sys.exit()

        if os.path.exists(virtualbox_dll):
            print("VirtualBox DLL Detected")
            sys.exit()

        if os.path.exists(vmware_dll):
            print("VirtualBox DLL Detected")
            sys.exit()

        try:
            sandboxie = ctypes.cdll.LoadLibrary("SbieDll.dll")
            print("Sandboxie DLL Detected")
            sys.exit()

        except:
            pass



    def mac_check(self):
        mac_address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        vmware_mac_list = ["00:05:69", "00:0c:29", "00:1c:14", "00:50:56"]
        if mac_address[:8] in vmware_mac_list:
            print("VMware MAC Address Detected")
            sys.exit()

if __name__ == '__main__':
    test = BypassVM()
    test.registry_check()
    test.process_and_files_check()
    test.mac_check()





