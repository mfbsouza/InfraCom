import socket

class MySocket(socket.socket):
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None):
        super().__init__(family, type, proto, fileno) #use the superclass init

    #For a dns query, before the domain, this function put the '1' flag. Which identifies that this is a query request
    def dnsQuery(self, domainString, dnsIP, dnsPort):
        message = "1" + domainString
        self.sendto(message.encode(), (dnsIP, dnsPort))

    #For a dns domain registration, before the domain, this function put the '0' flag. Which identifies that this is a domain registration request
    def dnsRegisterDomain(self, domainString, dnsIP, dnsPort):
        message = "0" + domainString
        self.sendto(message.encode(), (dnsIP, dnsPort))

    def sendArquive(self, arquive, conn: socket.socket, bufferSize = 1024):
        f = open(arquive,'rb')
        l = f.read(1024)
        while (l):
           conn.send(l)
           print('Sent ',repr(l))
           l = f.read(bufferSize)
        f.close()
        conn.send(0)
        print('Done sending')

    def recieveArquive(self, file_name, bufferSize = 1024):
        with open(file_name, 'wb') as f:
            print ('file opened')
            while True:
                print('receiving data...')
                data = self.recv(bufferSize)
                print('data=%s', (data))
                if not data:
                    break
                # write data to a file
                f.write(data)
        f.close()
        print('Successfully get the file')
    

    def recieveDataOfAnySize(self, bufferSize = 1024):
        while True:
            dataList = []
            print("Receiving data...")
            data = self.recv(bufferSize)
            print('data=%s', (data))
            dataStr = str(data)
            print(dataStr)
            if dataStr:
                break
            dataList.append(data)
        return b''.join(dataList)
