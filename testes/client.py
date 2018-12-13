from socket import AF_INET, SOCK_DGRAM
from MySocket import MySocket, MESSAGE_SIZE
from Segment import Segment

SERVER_HOST = ''
SERVER_PORT = 50004

# # # # # # # # # #
snd_base = 38       # # # # # # # # # # (random)
next_seq = snd_base
rcv_base = -1

state = "send_syn"

s = MySocket(AF_INET, SOCK_DGRAM)
while True:
    if state == "send_syn": # send connection request to server
        connection_request = Segment(next_seq, rcv_base, syn='1')
        s.send_segment(connection_request, rcv_base, (SERVER_HOST, SERVER_PORT))

        # wait for ack and port number

        state = "break"
    elif state == "break":
        state = "menu"
        break


while True:
    if state == "menu":
        # request menu
        request_msg = '0'

        segments, next_seq = s.fragment_message(request_msg, next_seq)
        for segment in segments:
            s.send_segment(segment, rcv_base, (SERVER_HOST, SERVER_PORT))

        # receive menu
        while True:
            ## receive segment
            data, addr = s.recvfrom(MESSAGE_SIZE)
            data = data.decode()

            segment = Segment(segment = data)
            segment.print()
            
            # stop receiving after last fragment
            if segment.last_frag == '1':
                break

        state = "break"

    elif state == "break":
        break