import socket
from Segment import Segment

MESSAGE_SIZE = 1024
HEADER_SIZE = 11
DATA_SIZE = MESSAGE_SIZE - HEADER_SIZE

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
        conn.send(b'$')
        print('Done sending')

    def recieveArquive(self, file_name, bufferSize = 1024):
        print('receiving data...')
        with open(file_name, 'wb') as f:
            done = False
            while not done:
                data = self.recv(bufferSize)
                if data.endswith(b'$'):
                    done = True
                    data = data[:len(data)-1]
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

    def send_segment(self, segment, ack_number, dest_addr):
        segment.set_ack_number(ack_number)
        self.sendto(segment.segment.encode(), dest_addr)

    # get a message of any size and return a list of fragments of that message, each one with the size equal to DATA_SIZE or smaller. Also adds a header to each fragment
    def fragment_message(self, msg, seq_number):
        segments = []
        
        while len(msg) > 0:
            if len(msg) < DATA_SIZE:
                segment = Segment(seq_number, data=msg[:(DATA_SIZE-1)])
            else:
                segment = Segment(seq_number, last_frag='0', data=msg[:(DATA_SIZE-1)])
            
            segments.append(segment)
            seq_number += 1
            msg = msg[DATA_SIZE:]

        # print('segments:\n')
        # for segment in segments:
        #     print(segment + '\n')

        return segments, seq_number