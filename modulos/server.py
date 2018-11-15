import socket

DNS_HOST = ''
DNS_PORT = 49152 # o numero de porta pode ser entre 49152 e 65535

# send IP and domain to DNS
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((DNS_HOST, DNS_PORT)) # solicitando conexao ao DNS
    s.sendall(b'0bois.com') # 0 -> code for DNS  |  bois.com -> domain
    data = s.recv(1024)
    print('Received', data.decode())