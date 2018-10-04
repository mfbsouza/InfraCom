# Servidor simples usando TCP/IP que só retorna pra o cliente o dados recebidos.

# pra nao precisar ficar referenciando a biblioteca direto (ex. socket.AF_INET)
# eu vou simplesmente importar tudo pra dentro do programa.
from socket import *

# definindo algumas constantes do servidor
HOST = ''       # host vazio eh basicamente traduzido pra o IP da maquina do server
PORT = 50007    # na função bind().
SIZE = 1024

# criação do scoket (a.k.a configurando o servidor):
# 1° parametro indica familia do endereço. AF_INET == Protocolo de endereço IP
# 2° parametro indica se é stream, ou datagram. SOCK_STREAM == Protocolo de transferencia TCP
# 3° parametro opicional, indica o Protocolo. Padrao é zero.
server_socket = socket(AF_INET, SOCK_STREAM)

# Agr vamos associar o scoket recém-criado a endereço e numero de porta
server_socket.bind((HOST, PORT))

# E agr vamos definir a quantidade de clientes que podem se conectar a esse socket
server_socket.listen(1)

while True:
    # basicamente o server fica em loop infinito aceitando pedidos de conexao.
    # Ao aceitar pedidos usando o metodo "accept", nos eh retornado um novo socket
    # que será usando como o "tubo de bytes" e o endereço do cliente.
    conn, addr = server_socket.accept()
    print('Conectado com:', addr)
    # enquanto existir uma comunicação entre cliente-servidor:
    while conn:
        dados = conn.recv(SIZE)
        # se o client parar de enviar dados vamos fechar a comunicação
        if not dados: break
        # devolve os dados recebidos do cliente
        conn.send(b'Eu sou servidor. Voce disse: ' + dados)
    # fecha a conexao
    conn.close()
