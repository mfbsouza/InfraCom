from socket import AF_INET, SOCK_DGRAM
from MySocket import MySocket, MESSAGE_SIZE
from Segment import Segment

# # # # # CONSTANTS # # # # #

DNS_HOST = ''
DNS_PORT = 49152

SELF_HOST = ''
SELF_PORT = 50004

MENU = '\n\nMENU\nDigite:\n1. Listar arquivos\n2. Solicitar arquivos\n3. Encerrar conexão\n'

# # # # # VARIABLES # # # # #

client_sockets = {}
state = "listen"

snd_base = 57       # # # # # # # # # # (random)
next_seq = snd_base
rcv_base = -1

# # # # # MAIN # # # # #

# send IP and domain to DNS
with MySocket(AF_INET, SOCK_DGRAM) as dns_socket:
    dns_socket.dnsRegisterDomain("bois.com", DNS_HOST, DNS_PORT)
    data = dns_socket.recv(MESSAGE_SIZE)
    print('Received', data.decode())
    dns_socket.close()

# connect to client
s = MySocket(AF_INET, SOCK_DGRAM)
s.bind((SELF_HOST, SELF_PORT))

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
