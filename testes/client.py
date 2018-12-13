from socket import AF_INET, SOCK_DGRAM
from MySocket import MySocket, MESSAGE_SIZE
from Segment import Segment

# # # # # CONSTANTS # # # # #

SERVER_HOST = ''
SERVER_PORT = 50004

# # # # # VARIABLES # # # # #

snd_base = 38       # # # # # # # # # # (random)
next_seq = snd_base
rcv_base = -1

state = "send_syn"

# # # # # MAIN # # # # #

s = MySocket(AF_INET, SOCK_DGRAM)
while True:
    if state == "send_syn": # send connection request to server
        connection_request = Segment(next_seq, syn='1')
        next_seq += 1
        s.send_segment(connection_request, rcv_base, (SERVER_HOST, SERVER_PORT))

        # wait for ack and new socket port number
        segment, rcv_base, client_addr = s.receive_segment(rcv_base)
        if segment.syn == '1' and segment.ack_number != -1:
            print('received SYN_ACK\n')
        
        state = "established"
    elif state == "established":
        # send ACK
        ack = Segment(next_seq, rcv_base)
        next_seq += 1
        s.send_segment(ack, rcv_base, (SERVER_HOST, SERVER_PORT))

        state = "break"
    elif state == "break":
        state = "menu"
        break


# while True:
#     if state == "menu":
#         # request menu
#         request_msg = '0'

#         segments, next_seq = s.fragment_message(request_msg, next_seq)
#         for segment in segments:
#             s.send_segment(segment, rcv_base, (SERVER_HOST, SERVER_PORT))

#         # receive menu
#         while True:
#             segment, rcv_base, addr = s.receive_segment(rcv_base)
            
#             # stop receiving after last fragment
#             if segment.last_frag == '1':
#                 break

#         state = "break"

#     elif state == "break":
#         break