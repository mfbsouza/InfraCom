from socket import AF_INET, SOCK_DGRAM
from MySocket import MySocket, MESSAGE_SIZE

SERVER_HOST = ''
SERVER_PORT = 50004

# # # # # # # # # #
snd_base = 38       # # # # # # # # # # (random)
next_seq = snd_base
rcv_base = 9999

state = "menu"

s = MySocket(AF_INET, SOCK_DGRAM)
while True:
    if state == "menu":
        # request menu
        request_msg = '0'
        s.send_message(request_msg, next_seq, rcv_base, (SERVER_HOST, SERVER_PORT))

        # receive menu
        while True:
            ## receive segment
            segment, addr = s.recvfrom(MESSAGE_SIZE)
            segment = segment.decode()

            # separate segment's fields
            seq_number = int(segment[:4])
            ack_number = int(segment[4:8])
            last_frag = segment[8]
            server_reply = segment[9:]

            print('seq_number:', seq_number)
            print('ack_number:', ack_number)
            print('last_frag:', last_frag)
            print('server_reply:', server_reply)

            # stop receiving after last fragment
            if last_frag == '1':
                break

        state = "break"

    elif state == "break":
        break