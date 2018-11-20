import socket
from MySocket import MySocket
import pickle

DNS_HOST = ''
DNS_PORT = 49152

server_PORT = 50000
SIZE = 1024     # ver isso!!

# send server's domain to DNS and get its IP
with MySocket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.dnsQuery("bois.com", DNS_HOST, DNS_PORT)
    data = s.recv(1024)

    if data.decode() == '-1':
        print('domain not found')
    else:
        server_HOST = data
        print('Received', data.decode())


# connect to server
socket_client = MySocket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((server_HOST, server_PORT))

d_files = socket_client.recv(SIZE*30)    # ajeitar tamanho!!
d_files = pickle.loads(d_files) # transform data in list

# print file_names
for i, file_name in enumerate(d_files):
    print(i, '-', file_name)

msg = input('Digite o número do arquivo desejado: ')
socket_client.send(msg.encode())

resposta = socket_client.recv(SIZE)
print(resposta.decode())

socket_client.close()
