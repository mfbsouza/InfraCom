from socket import AF_INET, SOCK_DGRAM
from MySocket import MySocket, MESSAGE_SIZE
from Segment import Segment

# # # # # CONSTANTS # # # # #

SERVER_HOST = ''
SERVER_PORT = 50004

# # # # # VARIABLES # # # # #

state = "menu"

# # # # # MAIN # # # # #

s = MySocket(AF_INET, SOCK_DGRAM)
# while True:
#     if state == "send_syn": # send connection request to server
#         connection_request = Segment(next_seq, syn='1')
#         next_seq += 1
#         s.send_segment(connection_request, rcv_base, (SERVER_HOST, SERVER_PORT))

#         # wait for ack and new socket port number
#         segment, client_addr = s.receive_segment()
#         if segment.syn == '1' and segment.ack_number != -1:
#             print('received SYN_ACK\n')
        
#         state = "established"
#     elif state == "established":
#         s.send_ack((SERVER_HOST, SERVER_PORT))

#         state = "break"
#     elif state == "break":
#         state = "menu"
#         break


while True:
    if state == "menu":
        # request menu
        request_msg = '0'
        s.send_message(request_msg, (SERVER_HOST, SERVER_PORT))

        # receive menu
        menu, addr = s.receive_message()
        print(menu)

        state = "break"

    elif state == "break":
        break