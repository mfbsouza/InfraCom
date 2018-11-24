import socket
from MySocket import MySocket
from os import listdir
import pickle

DNS_HOST = ''
DNS_PORT = 49152 # o numero de porta pode ser entre 49152 e 65535

self_HOST = ''
self_PORT = 50000
SIZE = 1024     # ver isso!!

# send IP and domain to DNS
with MySocket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.dnsRegisterDomain("bois.com", DNS_HOST, DNS_PORT)
    data = s.recv(1024)
    print('Received', data.decode())


# wait for clients
server_socket = MySocket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((self_HOST, self_PORT))
server_socket.listen(1)

conn, addr = server_socket.accept()
print('\nConnected to:', addr)

while True:
    menu = '\n\nMENU\nDigite:\n1. Listar arquivos\n2. Solicitar arquivos\n3. Encerrar conexão\n'
    menu = menu.encode() # turn str type into bytes
    conn.send(menu)

    client_choice = conn.recv(SIZE) # nao sabia qual parametro colocar
    client_choice = client_choice.decode()

    if client_choice == '1': # list files
        files = listdir('../arquivos')  # list all files at the folder 'arquivos'
        d_files = pickle.dumps(files)   # serialize files
        conn.sendall(d_files)              # send files' list to client
    elif client_choice == '2': # send file
        # send file
        dados = conn.recv(SIZE)
        if dados:
            choosenFile = int(dados.decode())
            print('choosen file:', files[choosenFile])
            print('sending file...')
            server_socket.sendArquive('../arquivos/' + files[choosenFile], conn, SIZE)
            print('file sent.')

        # while conn:
        #     dados = conn.recv(SIZE)     # receive data from client
        #     if not dados: break

        #     choosen_file = int(dados.decode())  # transform client's data in int
        #     print('choosen file:', files[choosen_file])

        #     file = open('../arquivos/' + files[choosen_file], "r")

        #     print('sending file...')
        #     d_file = file.read().encode()
        #     conn.send(d_file) # send choosen file to client
        #     print('file sent.')
    elif client_choice == '3': # connection closed
        conn.close()

    # conn.close()
