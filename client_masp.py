import socket, pickle, os
import win32security
import win32com.client, time
import platform
import psutil
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
    print("Successfully Connected")
except:
    print("ERROR WITH CONNECTION")
    exit()
#client.send(bytes('I am Client', 'utf8'))
close = True

username = os.getlogin() #os.environ.get('USERNAME')
expandname = os.path.expanduser('~')
sidstr = win32security.ConvertSidToStringSid(sid)
#hostname = socket.gethostname()
#IPAddr = socket.gethostbyname(hostname)
#test = ["hostname: ", hostname, '\n', "IPADDRESS: ", IPAddr, '\n']
#data_string = pickle.dumps(test)
#client.send(data_string)
while close:
    from_server = client.recv(4096)
    value = from_server.decode('utf8')
    print(value)
    #print(from_server.decode('utf8'))
    if value == 'E':
        client.close()
        close = False
    elif value == "U1":
        test = ["Username: ", username]
        data_string = pickle.dumps(test)
        client.send(data_string)
    elif value == "U2":
        test = ["SID: ", sidstr]
        data_string = pickle.dumps(test)
        client.send(data_string)
    elif value == "U4":
        test = ["Last Logon: ", logon]
        data_string = pickle.dumps(test)
        client.send(data_string)
    elif value == "O1":
        test = ["Machine Name: ", socket.gethostname()]
        data_string = pickle.dumps(test)
        client.send(data_string)
    elif value == "O2":
        test = ["Machine Version: ", platform.platform()]
        data_string = pickle.dumps(test)
        client.send(data_string)
    elif value == "O3":
        test = ["Machine Type: ", platform.machine()]
        data_string = pickle.dumps(test)
        client.send(data_string)
    elif value == "O4":
        test = ["Processor: ", platform.processor()]
        data_string = pickle.dumps(test)
        client.send(data_string)
    elif value == "C1":
        test = ["CPU status: ", psutil.cpu_percent(4)]
        data_string = pickle.dumps(test)
        client.send(data_string)
    elif value == "C2":
        output = os.popen('wmic process get description, processid').read()
        test = [output]
        data_string = pickle.dumps(test)
        client.send(data_string)
    elif value == "C3":
        test = list(psutil.win_service_iter())
        data_string = pickle.dumps(test)
        client.send(data_string)
    elif value == "M1":
        test = ["Memory Status: ", psutil.virtual_memory()]
        data_string = pickle.dumps(test)
        client.send(data_string)
    elif value == "M2":
        test = ["Memory Available: ", psutil.virtual_memory().available]
        data_string = pickle.dumps(test)
        client.send(data_string)






