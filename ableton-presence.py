import os
import re
import time
import win32gui
from pypresence import Presence

SLEEP = 10
CLIENT_ID = 1380506927125233866

def strip_not_responding(text):
    return re.sub(r"\s*\([^)]+\)\s*$", "", text)

def get_ableton_window_title():
    def enum_callback(hwnd, result):
        title = win32gui.GetWindowText(hwnd)
        if title.find(" - Ableton Live") != -1:
            result.append(title)
    result = []
    win32gui.EnumWindows(enum_callback, result)
    return strip_not_responding(result[0]) if result else None

RPC = Presence(client_id=CLIENT_ID)

print("Started, looking for Ableton")
os.system('title ableton-presence')

rpc_connected = False
lasttitle = ""
while True:
    title = get_ableton_window_title()

    if not title:
        if rpc_connected == True:
            print("Ableton closed, disconnecting RPC")
            RPC.close()
            rpc_connected = False
            lasttitle = ""
        time.sleep(SLEEP)
        continue

    if lasttitle == title.replace("*", ""):
        time.sleep(SLEEP)
        continue

    lasttitle = title.replace("*", "")

    version = title.split(" - ")[1].removesuffix("Lite")
    project = title.split(" ")[0].rstrip("*")

    if not rpc_connected:
        print(f"{version}opened, connnecting RPC")
        RPC.connect()
        rpc_connected = True
    print(f"New project: {project}")
    RPC.update(large_image="ableton-live", large_text=version,
               state=version, details=f"Project: {project}",
               party_id="music")

    time.sleep(SLEEP)
