# -*- coding: utf-8 -*-
import socket

HOST = ''
PORT = 49152 # o número de porta pode ser entre 49152 e 65535(?)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT)) 
while True:
    data, addr = s.recvfrom(1024)
    server_domain = data # deixa salvo dominio do servidor
    server_ip = addr[0] # deixa salvo ip do servidor
    print('received by', addr) # printa de quem recebeu (só pra teste)
    print(server_domain, server_ip) # printa o que recebeu (só pra teste)
    if not data: break
    s.sendto(data, addr) # entrega pro cliente (servidor) confirmando