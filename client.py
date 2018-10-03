from socket import *

serverHOST = 'localhost'
serverPORT = 50007
mensagem = [b'oi eae']

socket_client = socket(AF_INET, SOCK_STREAM)
socket_client.connect((serverHOST, serverPORT))
for x in mensagem:
    socket_client.send(x)
    resposta = socket_client.recv(1024)
    print('cliente recebeu: ', resposta)

socket_client.close()
