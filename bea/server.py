# -*- coding: utf-8 -*-
from udp_socket import SocketUDP
import utils
import socket
import pickle
from os import listdir

DNS_HOST = ''
DNS_PORT = 49152

self_HOST = ''
self_PORT = 50000

MENU = '\n\nMENU\nDigite:\n1. Listar arquivos\n2. Solicitar arquivos\n3. Encerrar conexão\n'

def listFiles():
    files = listdir('../arquivos') # list of available files
    list_of_files = ''

    for i, file in enumerate(files):
        list_of_files += '\n' + str(i) + ' - ' + file

    return list_of_files

if __name__ == "__main__":
# send IP and domain to DNS
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        domainString = "bois.com"
        message = "0" + domainString
        s.sendto(message.encode(), (DNS_HOST, DNS_PORT))
        data, addr = s.recvfrom(1024)
        print('Received', data.decode())

    # accept client's connection
    server = SocketUDP(self_PORT)
    addr = server.accept()
    msg  = server.recv_msg()
    server.send_msg("Connection established @ client side".encode())
    print(msg.decode())

    files = listdir('../arquivos') # list of available files

    while True: # reliable message trade
        server.send_msg(MENU.encode()) # send menu to client

        client_choice = server.recv_msg().decode()

        if client_choice == "1": # recieveListOfFiles
            list_of_files = listFiles()
            server.send_msg(list_of_files.encode())

        elif client_choice == "2": # recieveFile
            pass
        
        elif client_choice == "3": # closeConnection
            pass
            break