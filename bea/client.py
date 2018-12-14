from udp_socket import SocketUDP
import utils
import socket
import pickle

DNS_HOST = ''
DNS_PORT = 49152

server_HOST = ''
server_PORT = 50000

state = "requestServerIP" # initial state

if __name__ == "__main__":
    while True:
        if state == "requestServerIP":
            # send server's domain to DNS and get its IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                domainString = "bois.com"
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
            dFiles = client.recv_msg() # receive files' list from server
            dFiles = pickle.loads(dFiles) # transform data in list
            
            print('Available files:')
            for i, file_name in enumerate(dFiles): # print file_names
                print(i, '-', file_name)
            state = "menu" # goes back to menu
        
        elif state == "recieveFile":
            pass
        
        elif state == "closeConnection":
            pass
            status = "break"