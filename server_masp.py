import socket, pickle, psutil

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def startconn():
    serv.bind(('127.0.0.1', 2023))
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
        examvalue()
        #return

def examvalue():
    value = ""
    accepted_command = ["U", "O", "C", "M","E"]
    print("[U] User Enum \n"
          "[O] OS Enum \n"
          "[C] CPU Enum \n"
          "[M] Memory Enum \n"
          "[E] Exit \n")
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
        print("Connection Closed")
    else:
        print("Invalid Command")
    global ActualValue
    ActualValue = type + value
    connection()
    return

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
        examvalue()
    elif main_input == 2:
        print("Work in Progress")
    else:
        print("Not an option")



startconn()
main()
