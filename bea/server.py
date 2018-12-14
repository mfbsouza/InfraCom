from udp_socket import SocketUDP
if __name__ == "__main__":
    server = SocketUDP(1004)
    addr = server.accept()
    msg  = server.recv_msg()
    server.send_msg("olah, tudo bem?".encode())
    print(msg.decode())