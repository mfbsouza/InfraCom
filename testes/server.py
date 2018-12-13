from socket import AF_INET, SOCK_DGRAM
from MySocket import MySocket, MESSAGE_SIZE

SELF_HOST = ''
SELF_PORT = 50004

MENU = '\n\nMENU\nDigite:\n1. Listar arquivos\n2. Solicitar arquivos\n3. Encerrar conexão\n'

# # # # # # # # # #
snd_base = 57       # # # # # # # # # # (random)
next_seq = snd_base
rcv_base = -1

s = MySocket(AF_INET, SOCK_DGRAM)
s.bind((SELF_HOST, SELF_PORT))

while True:
    ## receive segment
    segment, addr = s.recvfrom(MESSAGE_SIZE)
    segment = segment.decode()

    # separate segment's fields
    seq_number = int(segment[:4])
    ack_number = int(segment[4:8])
    last_frag = segment[8]
    ack_valid = segment[9]
    client_choice = segment[10:]

    print('seq_number:', seq_number)
    print('ack_number:', ack_number)
    print('last_frag:', last_frag)
    print('ack_valid:', ack_valid)
    print('client_choice:', client_choice)

    ## analyze segment
    # if first contact
    if rcv_base == -1:
        rcv_base = seq_number

    if client_choice == '0':    # send menu
        # next_seq = s.send_message(MENU, next_seq, rcv_base, addr)

        segments, next_seq = s.fragment_message(MENU, next_seq)
        for segment in segments:
            s.send_segment(segment, rcv_base, addr)

        print('Sent menu')

    # if ack_number == next_seq:  # can send
