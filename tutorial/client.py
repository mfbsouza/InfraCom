from socket import *

# definindo informações do servidor que vamos conectar.
serverHOST = 'localhost'
serverPORT = 50007
SIZE= 1024

# cria o socket cliente
socket_client = socket(AF_INET, SOCK_STREAM)

# pede para o servidor para estabelecer uma conexao.
socket_client.connect((serverHOST, serverPORT))

# A partir daqui, se tudo der certo com o servidor, ele criou um "tubo de dados"
# com o nosso socket. Vamos enviar algo para testar:
msg = input('Digite uma mensagem para o servidor: ')
# vamos pegar a mensagem, transformar pra bytes e mandar para o servidor.
socket_client.send(msg.encode())

# A partir daqui, o servidor recebeu nossa msg e se tudo der certo ele vai responder
resposta = socket_client.recv(SIZE)
# transforma resposta pra string e printa
print(resposta.decode())

# fecha a conexao
socket_client.close()
