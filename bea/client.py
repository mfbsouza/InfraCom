from udp_socket import SocketUDP

if __name__ == "__main__":
    client = SocketUDP()
    client.connect('localhost', 1004)
    client.send_msg("oie".encode())
    print(client.recv_msg().decode())