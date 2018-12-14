# -*- coding: utf-8 -*-
from udp_socket import SocketUDP
import utils
import socket
import pickle

DNS_HOST = ''
DNS_PORT = 49152

server_HOST = ''
server_PORT = 50000

state = "requestServerIP" # initial state

list_of_files = ''

def getFileName(file_number):
    if len(list_of_files) > 0:
        files = list_of_files.split('\n')[1:]   # files: [i - fileName.txt]
        return files[file_number-1].split(' - ')[1]
    else:
        return ''

if __name__ == "__main__":
    while True:
        if state == "requestServerIP":
            # send server's domain to DNS and get its IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                domainString = input('Enter the domain you want to access: ')
                message = "1" + domainString
                s.sendto(message.encode(), (DNS_HOST, DNS_PORT))
                dns_data, addr = s.recvfrom(1024)

                if dns_data.decode() == '-1':
                    print('Error: Domain not found')
                    state = "domainNotFound"
                else:
                    server_HOST = dns_data # saves server IP

                    client = SocketUDP()
                    client.connect(server_HOST, server_PORT)
                    client.send_msg("Connection established @ server side".encode())
                    print(client.recv_msg().decode())

                    state = "menu"

        elif state == "domainNotFound":
            m = str(input("Do you want to try to request the domain to the DNS server again? yes(y) or no(n)\n"))
            if m == "y":
                state = "requestServerIP"
            elif m == "n":
                state = "break"
        
        elif state == "break":
            break
        
        elif state == "menu":
            # receive menu and send choice
            menu = client.recv_msg().decode()
            print(menu)
            choice = str(input("\nType your choice's number\n"))
            client.send_msg(choice.encode())

            if choice == "1":
                state = "recieveListOfFiles"
            elif choice == "2":
                state = "recieveFile"
            elif choice == "3":
                state = "closeConnection"

        elif state == "recieveListOfFiles":
            list_of_files = client.recv_msg().decode()
            print(list_of_files)

            state = "menu" # goes back to menu
        
        elif state == "recieveFile":
            # send the name of the chosen file
            file_number = int(input('\nWhich one do you want? '))
            file_name = getFileName(file_number)

            client.send_msg(file_name.encode())
            print('\nWaiting for file...')

            # receive file
            file_data = client.recv_msg()
            # save file
            f = open('../arquivos/cliente/' + file_name, 'wb')
            f.write(file_data)
            f.close()
            print('Received file, saved as', file_name)
            
            state = "menu" # goes back to menu
        
        elif state == "closeConnection":
            pass
            status = "break"