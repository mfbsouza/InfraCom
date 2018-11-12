import socket

HOST = ''
PORT = 49152 # o numero de porta pode ser entre 49152 e 65535

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((HOST, PORT)) # solicitando conexao ao DNS
    s.sendall(b'bois.com')
    data = s.recv(1024)
    print('Received', data.decode())