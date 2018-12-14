from udp_socket import SocketUDP
import utils
import socket
from archives import *

DNS_HOST = ''
DNS_PORT = 49152

self_HOST = ''
self_PORT = 50000

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

    files = Archives(empty=False)
    files_list_msg = ""
    i = 0
    for element in files.archive_list:
        if files_list_msg == "":
            files_list_msg = '1' + ' ' + element.title + "\n"
        else:
            files_list_msg = files_list_msg + str(i) + ' ' + element.title + "\n"
        i = i + 1

    while True:
        client_choice  = server.recv_msg()
        client_choice = client_choice.decode()
        print(client_choice)

        if client_choice == '1': # list files
            print(files_list_msg)
            server.send_msg(files_list_msg.encode())
            
        elif client_choice == '2': # send file
            # send file
            dados = server.recv_msg()
            if dados:
                choosenFile = int(dados.decode()) - 1
                print('choosen file:', files.archive_list[choosenFile])
                print('sending file...')
                server.send_msg(files.archive_list[choosenFile].body.encode())
                print('file sent.')

        # elif client_choice == '3': # connection closed
        #     conn.close()
        #     break


    # make message trade