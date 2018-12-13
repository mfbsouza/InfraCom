from socket import AF_INET, SOCK_DGRAM
from MySocket import MySocket, MESSAGE_SIZE
from Segment import Segment
from Helper import *

SELF_HOST = ''
SELF_PORT = 50004

MENU = '\n\nMENU\nDigite:\n1. Listar arquivos\n2. Solicitar arquivos\n3. Encerrar conexão\n'

client_sockets = {}
state = "listen"

# # # # # # # # # #
snd_base = 57       # # # # # # # # # # (random)
next_seq = snd_base
rcv_base = -1

s = MySocket(AF_INET, SOCK_DGRAM)
s.bind((SELF_HOST, SELF_PORT))

# connect to client
while True:
    if state == "listen":   # wait for connection request
        data, addr = s.recvfrom(MESSAGE_SIZE)
        data = data.decode()

        segment = Segment(segment=data)
        segment.print()

        if segment.syn == '1':
            tube_socket = MySocket(AF_INET, SOCK_DGRAM)
            tube_socket.bind((SELF_HOST, SELF_PORT+1))  # make port number random and check if it already exists

            # send ack
            # send port number
            
        state = "break"
    elif state == "break":
        break


while True:
    ## receive segment
    data, addr = s.recvfrom(MESSAGE_SIZE)
    data = data.decode()

    segment = Segment(segment = data)
    segment.print()

    ## analyze segment
    # if first contact
    if rcv_base == -1:
        rcv_base = segment.seq_number

    if segment.data == '0':    # send menu
        segments, next_seq = s.fragment_message(MENU, next_seq)
        for segment in segments:
            s.send_segment(segment, rcv_base, addr)

        print('Sent menu')

    # if ack_number == next_seq:  # can send
