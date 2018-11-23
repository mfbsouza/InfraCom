import socket
from MySocket import MySocket
import pickle

DNS_HOST = ''
DNS_PORT = 49152

server_HOST = ''
server_PORT = 50000
SIZE = 1024     # ver isso!!

# send server's domain to DNS and get its IP
with MySocket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.dnsQuery("bois.com", DNS_HOST, DNS_PORT)
    data = s.recv(1024)

    if data.decode() == '-1':
        print('Error: Domain not found')
    else:
        server_HOST = data
        # print('Received', data.decode())


# connect to server
socket_client = MySocket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((server_HOST, server_PORT))

while True:
    menu_server = socket_client.recv(SIZE) # não sabia qual parametro colocar
    menu_server = menu_server.decode() # turn bytes into str

    print(menu_server)

    choice = str(input('\nSua escolha:\n'))

    socket_client.send(choice.encode())

    if choice == '1': # asks to list files
        d_files = socket_client.recv(SIZE*30)    # receive files' list from server | ajeitar tamanho!!
        d_files = pickle.loads(d_files) # transform data in list


        print('Available files:')

        # print file_names
        for i, file_name in enumerate(d_files):
            print(i, '-', file_name)
        
    elif choice == '2': # wants to receive a file
        msg = input('\nWhich one do you want? ')
        socket_client.send(msg.encode())

        print('\nwaiting for file...')
        d_file = socket_client.recv(SIZE)
        print('received file:\n')
        print(d_file.decode())

    elif choice == '3':
        socket_client.close() # connection closed