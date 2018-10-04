# Simples servidor Echo usando TCP/IP
 Basicamente o servidor fica num loop infinito esperando cliente querendo se conectar.
 Quando um cliente pede conexao o servidor cria um novo socket que vai ser usado como um "tubo de dados"
## Executando
    para testar, execute primeiro o servidor, depois o cliente
    ```bash
    python3 server.py
    python3 client.py
    ```
![pic](pic.png)
