
import socket
import select
import sys

class ipClient():
    def __init__(self, serverAddr, serverPort, serverKey):
        self.serverAddr = (serverAddr,int(serverPort))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverKey = serverKey

    def connect(self):
        return self.sock.connect(self.serverAddr)

    def authenticate(self):
        #print self.receive()
        self.send(self.serverKey)
        response = self.receive()
        if response != "authenticatesuccess":
            self.close
            return 1

    def communicate(self):
        sockList = [sys.stdin, self.sock]
        readSock, writeSock, errorSock = select.select(sockList, [], [])
        for sock in readSock:
            if sock == self.sock:
                data = self.receive()
                if not data:
                    print "Disconnected from server."
                    return 1
                else:
                    print data
            else:
                message = raw_input("?")
                self.send(message)

    def send(self, message):
        return self.sock.sendall(message)

    def receive(self, buf=4096):
        #print buf
        return self.sock.recv(buf)

    def close(self):
        return self.sock.close()

    def serverAddr(self):
        return self.serverAddr

    def serverSock(self):
        return self.sock
