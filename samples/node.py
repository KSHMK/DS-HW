import socketserver
import socket
import requests
import os
import queue
import threading
from struct import unpack
from win32com.client import GetObject
from subprocess import getoutput as go

SERVER = "http://192.168.5.100:8080"
AV_NAME = ""
DOWNLOAD_PATH = "download"

task_list = queue.Queue()

def register_node():
    global AV_NAME
    objWMI = GetObject('winmgmts:\\\\.\\root\\SecurityCenter2').InstancesOf('AntiVirusProduct')
    for obj in objWMI:
        AV_NAME = obj.displayName
    
    data = {}
    data["av_name"] = AV_NAME

    requests.post(SERVER+"/node",json=data)

def download_file(filename):
    r = requests.get(SERVER+"/sample/"+filename)
    f = open(os.path.join(DOWNLOAD_PATH,filename),"wb")
    f.write(r.content)
    f.close()

def setting_env():
    file_exists = os.path.exists(os.path.join(DOWNLOAD_PATH, "7za.exe"))
    if not file_exists:
        download_file("7za.exe")
    
    file_exists = os.path.exists(os.path.join(DOWNLOAD_PATH, "run.bat"))
    if not file_exists:
        download_file("run.bat")

def run_sample(filename):
    is_virus = False
    setting_env()
    download_file(filename+".zip")
    go(os.path.join(DOWNLOAD_PATH, "run.bat")+" "+filename+".zip")
    if not os.path.exists(os.path.join(DOWNLOAD_PATH, filename)):
        is_virus = True
    else:
        try:
            f = open(os.path.join(DOWNLOAD_PATH, filename),"rb")
            f.close()   
        except Exception as e:
            is_virus = True
        os.remove(os.path.join(DOWNLOAD_PATH, filename))
    os.remove(os.path.join(DOWNLOAD_PATH, filename+".zip"))
    return is_virus

def check_task_list():
    while True:
        filename = task_list.get().decode()
        is_exist = run_sample(filename)
        requests.put(SERVER+"/node",json={"sample_hash":filename,"av_name":AV_NAME,"detect_result":is_exist})
        task_list.task_done()

def check_task_init():
    if not os.path.exists(os.path.join(DOWNLOAD_PATH)):
        os.mkdir(DOWNLOAD_PATH)
    register_node()
    threading.Thread(target=check_task_list, daemon=True).start()

class ThreadingTCPReqHandle(socketserver.BaseRequestHandler):
    def handle(self):
        sock: socket.socket = self.request
        sock.settimeout(4)
        try:
            recv_len = unpack("<I",sock.recv(4))[0]
            file_name = sock.recv(recv_len)
            task_list.put(file_name)
        except socket.timeout:
            pass
        sock.close()
        

class ThreadingTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass

if __name__ == "__main__":
    check_task_init()
    server = ThreadingTCPServer(("0.0.0.0", 8080),ThreadingTCPReqHandle)
    with server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        server.shutdown()