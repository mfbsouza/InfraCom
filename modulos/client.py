import socket
from MySocket import MySocket

DNS_HOST = ''
DNS_PORT = 49152

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

socket_client.getFilesList(SIZE)
socket_client.sendFileRequest()
socket_client.getRequestedFile(SIZE)

socket_client.close()
