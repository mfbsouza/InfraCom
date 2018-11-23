import socket
from os import listdir
import pickle

class MySocket(socket.socket):
    def __init__(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0, fileno=None):
        super().__init__(family, type, proto, fileno) #use the superclass init

    #For a dns query, before the domain, this function put the '1' flag. Which identifies that this is a query request
    def dnsQuery(self, domainString, dnsIP, dnsPort):
        message = "1" + domainString
        self.sendto(message.encode(), (dnsIP, dnsPort))

    #For a dns domain registration, before the domain, this function put the '0' flag. Which identifies that this is a domain registration request
    def dnsRegisterDomain(self, domainString, dnsIP, dnsPort):
        message = "0" + domainString
        self.sendto(message.encode(), (dnsIP, dnsPort))

    # Send files' list from the server to the client
    def sendFilesList(self, files, conectionSocket):
        files[:] = listdir('../arquivos')   # list all files at the folder 'arquivos'
        d_files = pickle.dumps(files)       # serialize files
        conectionSocket.send(d_files)       # send files' list to client

    # Send requested file from the server to the client
    def sendRequestedFile(self, files, connectionSocket, clientInput):
        fileIndex = int(clientInput.decode())
        print('requested file:', files[fileIndex])

        file = open('../arquivos/' + files[fileIndex], "r")

        print('sending file...')
        d_file = file.read().encode()
        connectionSocket.send(d_file) # send choosen file to client
        print('file sent.')

    # Receive files' list from server
    def getFilesList(self, SIZE):
        d_files = self.recv(SIZE)
        files = pickle.loads(d_files) # transform data in list

        print('Available files:')
        for i, file_name in enumerate(files):
            print(i, '-', file_name)

    # Send the number of the wanted file to the server
    def sendFileRequest(self):
        msg = input('\nWanted file number: ')
        self.send(msg.encode())
        print('\nwaiting for file...')

    # Receive the requested file from the server
    def getRequestedFile(self, SIZE):
        d_file = self.recv(SIZE)
        print('received file:\n')
        print(d_file.decode())