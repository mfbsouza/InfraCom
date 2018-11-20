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
while True:
    conn, addr = server_socket.accept()
    print('Conectado com:', addr)

    files = listdir('../arquivos')  # list all files at the folder 'arquivos'
    d_files = pickle.dumps(files)   # serialize files
    conn.send(d_files)              # send files' list to client

    while conn:
        dados = conn.recv(SIZE)     # receive data from client
        if not dados: break
        conn.send(b'Eu sou servidor. Voce disse: ' + dados)

        choosen_file = int(dados.decode())  # transform client's data in int

        print('arquivo escolhido:', files[choosen_file])

    conn.close()
