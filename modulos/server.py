import socket
from MySocket import MySocket

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
    print('\nConnected to:', addr)

    files = []
    s.sendFilesList(files, conn)

    while conn:
        dados = conn.recv(SIZE)     # receive data from client
        if not dados: break

        s.sendRequestedFile(files, conn, dados)

    conn.close()
