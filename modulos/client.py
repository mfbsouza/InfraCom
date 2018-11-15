import socket

DNS_HOST = ''
DNS_PORT = 49152

# send server's domain to DNS and get its IP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((DNS_HOST, DNS_PORT))
    s.sendall(b'1bois.com') # 1 -> code for DNS  |  bois.com -> domain
    data = s.recv(1024)

    if data.decode() == '-1':
        print('domain not found')
    else:
        print('Received', data.decode())
