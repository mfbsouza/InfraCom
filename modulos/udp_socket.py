import socket
import random
from multiprocessing import Process
from multiprocessing import Value
from threading import Thread
from queue import Queue
from utils import Package

class SocketUDP:
    def __init__(self, port=0):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind(('', port))

        self.__other_addr = None
        self.__other_seq = 0
        self.__seq = random.randint(0, 1024)

        self.__send_buffer = Queue()
        self.__recv_buffer = Queue()
        self.__acks_buffer = Queue()

    def start(self):
        Thread(target=SocketUDP.recv_loop, args=(self.__socket, self.__acks_buffer, self.__recv_buffer, self.__send_buffer, self.__other_addr)).start()
        Thread(target=SocketUDP.send_loop, args=(self.__socket, self.__send_buffer, self.__acks_buffer, self.__other_addr)).start()

    def connect(self, host, port):
        addr = (host, port)
        if self.handshake(addr):
            self.start()
        else:
            raise Exception("Could Not connect")

    def handshake(self, addr):
        syn_msg = Package(self.__seq, 0, False, True, True).encode()
        cur_try = 0
        other_seq = None
        while cur_try < Package.NUMBER_OF_RETRIES: # checks deadlock, tries 5 times
            self.__socket.sendto(syn_msg, addr)
            shared_other_seq = Value('i')
            recv_thrd = Process(target=SocketUDP.recv_syn_res, args=(self.__socket, shared_other_seq))
            recv_thrd.start()
            recv_thrd.join(1)
            if recv_thrd.is_alive():
                recv_thrd.terminate()
                recv_thrd.join()
                cur_try += 1
            else:
                other_seq = shared_other_seq.value
                break
        if other_seq is not None:
            self.__other_addr = addr
            self.__other_seq = other_seq
            self.__socket.sendto(Package(self.__seq, self.__other_seq + 1, True, False, True).encode(), addr)
            return True
        else:
            return False

    def accept(self):
        while True:
            data, other = self.__socket.recvfrom(1024)
            package = Package.decode(data)
            if not package.is_syn:
                continue
            self.__other_addr = other
            self.__other_seq = package.seq
            self.start()
            self.__send_buffer.put(Package(self.__seq, 0, False, True, True))
            return other
            
    @staticmethod
    def recv_syn_res(sock, shared_other_seq):
        data, other = sock.recvfrom(1024)
        shared_other_seq.value = Package.decode(data).seq

    def send_msg(self, msg):
        begin = 0
        while begin < len(msg):
            end = begin + Package.MAX_DATA_SIZE
            data = msg[begin:end]
            self.__seq += 1
            is_end = end >= len(msg)
            self.__send_buffer.put(Package(self.__seq, 0, False, False, is_end, data))
            begin = end
    
    def recv_msg(self):
        data = b''
        while True:
            package = self.__recv_buffer.get()
            if package.seq <= self.__other_seq:
                continue
            self.__other_seq = package.seq
            data += package.data
            if package.is_end:
                break
        return data
    
    @staticmethod
    def send_loop(sock, send_buffer, acks_buffer, to_addr):
        while True:
            msg = send_buffer.get()
            # if msg.content().decode() == "close": # if msg content is "close", get out of the loop, thread dies
            #     break
            ok = False
            cur_try = 0
            while cur_try < Package.NUMBER_OF_RETRIES:
                sock.sendto(msg.encode(), to_addr)
                try:
                    ack = acks_buffer.get(True, 1)
                    if ack.ack > msg.seq:
                        ok = True
                        break
                except Exception:
                    cur_try += 1
                    pass
            if not ok:
                raise Exception(str(to_addr) + " is not responding :/")


    @staticmethod
    def recv_loop(sock, acks_buffer, recv_buffer, send_buffer, to_addr):
        while True:
            data, client = sock.recvfrom(1024)
            package = Package.decode(data)
            if package.is_ack:
                acks_buffer.put(package)
            elif package.is_syn:
                sock.sendto(Package(0, package.seq + 1, True, False, False).encode(), to_addr)
            # elif data.decode()[-5:] == "close":
            #     break
            else:
                recv_buffer.put(package)
                sock.sendto(Package(0, package.seq + 1, True, False, False).encode(), to_addr)