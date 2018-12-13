import socket
from Segment import Segment

MESSAGE_SIZE = 1024
HEADER_SIZE = 11
DATA_SIZE = MESSAGE_SIZE - HEADER_SIZE

class MySocket(socket.socket):
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None):
        super().__init__(family, type, proto, fileno) #use the superclass init

        self.next_seq = 0
        self.next_ack = 0

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

    # get a message of any size and return a list of fragments of that message, each one with the size equal to DATA_SIZE or smaller. Also adds a header to each fragment
    def fragment_message(self, msg):
        segments = []
        
        while len(msg) > 0:
            if len(msg) < DATA_SIZE:
                segment = Segment(self.next_seq, data=msg[:(DATA_SIZE-1)])
            else:
                segment = Segment(self.next_seq, last_frag='0', data=msg[:(DATA_SIZE-1)])
            
            segments.append(segment)
            msg = msg[DATA_SIZE:]

        return segments

    def receive_message(self):
        msg = ''

        while True:
            segment, addr = self.receive_segment()

            if segment.seq_number == self.next_ack:
                msg = msg + segment.data

                self.send_ack(self.next_ack, addr)

                if self.next_ack == 0:
                    self.next_ack = 1
                else:
                    self.next_ack = 0

                if segment.last_frag == '1':
                    break

        return msg, addr

    def receive_segment(self):
        data, addr = self.recvfrom(MESSAGE_SIZE)
        data = data.decode()

        segment = Segment(segment=data)

        print('received:')
        segment.print()

        return segment, addr

    def send_ack(self, ack_nunmber, dest_addr):
        ack = Segment(ack_number=ack_nunmber)
        self.sendto(ack.segment.encode(), dest_addr)

    # send msg with any size to a destination   (fragment the msg, send it and wait for ACK)
    def send_message(self, msg, dest_addr):
        segments = self.fragment_message(msg)

        if self.next_seq == 0:
            state = "send_0"
        else:
            state = "send_1"

        i = 0
        while True:
            if state == "send_0":
                self.sendto(segments[i].segment.encode(), dest_addr)
                self.next_seq = 1

                state = "wait_for_ack_0"
            elif state == "wait_for_ack_0":
                ack, addr = self.receive_segment()
                
                if ack.ack_number == 0:
                    print('received ack 0')
                    i += 1
                    state = "send_1"
            elif state == "send_1":
                self.sendto(segments[i].segment.encode(), dest_addr)
                self.next_seq = 0

                state = "wait_for_ack_1"
            elif state == "wait_for_ack_1":
                ack = self.receive_segment()

                if ack.ack_number == 1:
                    print('received ack 1')
                    i += 1
                    state = "send_0"
            elif state == "break":
                break

            if i >= len(segments):
                break