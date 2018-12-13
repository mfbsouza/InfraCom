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

# # # # # MAIN # # # # #

# send IP and domain to DNS
with MySocket(AF_INET, SOCK_DGRAM) as dns_socket:
    dns_socket.dnsRegisterDomain("bois.com", DNS_HOST, DNS_PORT)
    data = dns_socket.recv(MESSAGE_SIZE)
    print('Received', data.decode())
    print()
    dns_socket.close()

# connect to client
s = MySocket(AF_INET, SOCK_DGRAM)
s.bind((SELF_HOST, SELF_PORT))

# while True:
#     if state == "listen":
#         # wait for connection request
#         segment, client_addr = s.receive_segment()

#         if segment.syn == '1':
#             # create new socket
#             tube_socket_port = SELF_PORT+1  # make port number random and check if it already exists
#             tube_socket = MySocket(AF_INET, SOCK_DGRAM)
#             tube_socket.bind((SELF_HOST, tube_socket_port))

#             # # send ACK with socket port number
#             # syn_ack_data = str(tube_socket_port)
#             # syn_ack = Segment(next_seq, rcv_base, syn='1', data=syn_ack_data)
#             # next_seq += 1
#             # s.send_segment(syn_ack, rcv_base, client_addr)

#         state = "syn_rcvd"
#     elif state == "syn_rcvd":
#         # wait for ACK
#         segment, client_addr = s.receive_segment()
#         print('received ACK\n')

#         state = "break"
#     elif state == "break":
#         break


while True:
    segment, client_addr = s.receive_message()

    if segment == '0':    # send menu
        s.send_message(MENU, client_addr)

        print('Sent menu')