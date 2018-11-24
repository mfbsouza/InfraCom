import socket

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

    def sendArquive(self, arquive):
        print()

    def reciveArquive(self):
        print()

    def recieveDataOfAnySize(self):
        print()