import ctypes
import os
import pickle
import platform
import socket
import subprocess

import psutil
import win32com.client
import win32security

strComputer = "."
objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_NetworkLoginProfile")



def Convert_to_human_time(dtmDate):

    strDateTime = ""

    if dtmDate[4] == 0:
        strDateTime = dtmDate[5] + '/'

    else:
        strDateTime = dtmDate[4] + dtmDate[5] + '/'

    if dtmDate[6] == 0:
        strDateTime = strDateTime + dtmDate[7] + '/'

    else:
        strDateTime = strDateTime + dtmDate[6] + dtmDate[7] + '/'
        strDateTime = strDateTime + dtmDate[0] + dtmDate[1] + dtmDate[2] + dtmDate[3] + " " + dtmDate[8] + dtmDate[9] + ":" + dtmDate[10] + dtmDate[11] +':' + dtmDate[12] + dtmDate[13]

    return strDateTime

for objItem in colItems:
    if objItem.LastLogon is not None:
         logon = Convert_to_human_time(objItem.LastLogon)

SERVERIP = '127.0.0.1' #EDIT server IP here !!!!!!!!!!!!!!!!!!!

desc = win32security.GetFileSecurity(
    ".", win32security.OWNER_SECURITY_INFORMATION
)
sid = desc.GetSecurityDescriptorOwner()

# https://www.programcreek.com/python/example/71691/win32security.ConvertSidToStringSid
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((SERVERIP, 2023))
except:
    print("ERROR WITH CONNECTION")
    exit()
else:
    print("Successfully Connected")
#client.send(bytes('I am Client', 'utf8'))
close = True

username = os.getlogin() #os.environ.get('USERNAME')
expandname = os.path.expanduser('~')
sidstr = win32security.ConvertSidToStringSid(sid)
#hostname = socket.gethostname()
#IPAddr = socket.gethostbyname(hostname)
#action = ["hostname: ", hostname, '\n', "IPADDRESS: ", IPAddr, '\n']
#data_string = pickle.dumps(action)
#client.send(data_string)


def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
        print(os.getuid())
    except AttributeError:
       is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


while close:
    from_server = client.recv(4096)
    prevalue = from_server.decode('utf-8')
    value = prevalue.split()[0]
    print(value)
    #print(from_server.decode('utf8'))
    if value == 'E':
        client.close()
        close = False
    elif value == "U1":
        action = ["Username: ", username]
        data_string = pickle.dumps(action)
        client.send(data_string)
    elif value == "U2":
        action = ["SID: ", sidstr]
        data_string = pickle.dumps(action)
        client.send(data_string)
    elif value == "U4":
        action = ["Last Logon: ", logon]
        data_string = pickle.dumps(action)
        client.send(data_string)
    elif value == "O1":
        action = ["Machine Name: ", socket.gethostname()]
        data_string = pickle.dumps(action)
        client.send(data_string)
    elif value == "O2":
        action = ["Machine Version: ", platform.platform()]
        data_string = pickle.dumps(action)
        client.send(data_string)
    elif value == "O3":
        action = ["Machine Type: ", platform.machine()]
        data_string = pickle.dumps(action)
        client.send(data_string)
    elif value == "O4":
        action = ["Processor: ", platform.processor()]
        data_string = pickle.dumps(action)
        client.send(data_string)
    elif value == "C1":
        action = ["CPU status: ", psutil.cpu_percent(4)]
        data_string = pickle.dumps(action)
        client.send(data_string)
    elif value == "C2":
        output = os.popen('wmic process get description, processid').read()
        action = [output]
        data_string = pickle.dumps(action)
        client.send(data_string)
    elif value == "C3":
        action = list(psutil.win_service_iter())
        listvalue = []
        for excess in action:
            listvalue.append((str(excess.name())))

        data_string = pickle.dumps(listvalue)
        client.send(data_string)
    elif value == "M1":
        action = ["Memory Status: ", str(psutil.virtual_memory())]
        data_string = pickle.dumps(action)
        client.send(data_string)
    elif value == "M2":
        action = ["Memory Available: ", psutil.virtual_memory().available]
        data_string = pickle.dumps(action)
        client.send(data_string)
    elif value == "F1":
        action = subprocess.check_output('netsh advfirewall show allprofiles', shell=True)
        client.send(action)
    elif value == "F2":
        if isAdmin():
            try:
                action = subprocess.check_call('netsh advfirewall set allprofile state off')
                client.send(bytes("Disabled","utf8"))
            except:
                client.send(bytes("Error Found, not admin","utf8"))
        else:
            client.send(bytes("Not admin", "utf8"))
    elif value == "39":
        os.system("shutdown /s /t 00")
    elif value == "22":
        print(prevalue)
        processName = prevalue.split()[1]
            #print(processName)
        while True:
            for proc in psutil.process_iter():
                if proc.name() == processName:
                    #client.send(pickle.dumps("Process Terminated"))
                #print("Killed")
                    proc.kill()
                    break
                #client.send(pickle.dumps("Process terminated"))
                else:
                #client.send(pickle.dumps("Process terminated"))
                    pass
        #client.send(pickle.dumps("No process found"))
