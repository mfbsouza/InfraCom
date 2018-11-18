import socket
from MySocket import MySocket

DNS_HOST = ''
DNS_PORT = 49152 # o numero de porta pode ser entre 49152 e 65535

# send IP and domain to DNS
with MySocket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.dnsRegisterDomain("bois.com", DNS_HOST, DNS_PORT)
    data = s.recv(1024)
    print('Received', data.decode())