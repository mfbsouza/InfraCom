import socket
from MySocket import MySocket

DNS_HOST = ''
DNS_PORT = 49152

# send server's domain to DNS and get its IP
with MySocket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.dnsQuery("bois.com", DNS_HOST, DNS_PORT)
    data = s.recv(1024)

    if data.decode() == '-1':
        print('domain not found')
    else:
        print('Received', data.decode())
