# -*- coding: utf-8 -*-
import socket

HOST = ''
PORT = 49152 # o número de porta pode ser entre 49152 e 65535

server = None

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    data, addr = s.recvfrom(1024)

    data_str = data.decode()
    code = data_str[0]
    msg = data_str[1:]

    if code == '0':
        server_domain = msg # deixa salvo dominio do servidor
        server_ip = addr[0] # deixa salvo ip do servidor
        
        server = (server_domain, server_ip)
        
        if not data: break
        s.sendto(data, addr) # entrega pro cliente (servidor) confirmando

        print('server', addr, 'with domain', server[0], 'has been saved')
    elif code == '1':
        if server and msg == server[0]:
            if not data: break
            s.sendto(server[1].encode(), addr) # send server's IP to client

            print('IP address', server[1], 'for domain', server[0], 'has been sent')
        else:
            if not data: break
            s.sendto(b'-1', addr) # send error code

            print('domain not found')
    else:
        if not data: break
        s.sendto(b'-1', addr) # send error code

        print('Error:', code, 'is not a valid code')