# TCP Echo Server using threading example
# based on http://stackoverflow.com/questions/17453212/multi-threaded-tcp-server-in-python

import socket # needed for connections
import threading # needed for multithreading
import Queue # needed to share data between threads
import json

passwords = ['1122334455']

class AggregateThread(threading.Thread):
    def __init__(self, in_queue):
        threading.Thread.__init__(self)
        self.kill_received = False
        self.in_q = in_queue
        print "[+] New thread starting for aggregation."

    def run(self):
        while not self.kill_received:
            cur_in = self.in_q.get()
            print "Agg: " + cur_in[0] + json.dumps(cur_in[1]) + "."
            ## THIS IS WHERE I NEED TO DO THE ADDING TO DATABASES PROBABLY
            self.in_q.task_done()

    def shutdown(self):
        self.in_q.put("")
        print "[-] Aggregation thread closing."


class ClientThread(threading.Thread):
    def __init__(self, ip, port, socket, out_queue):
        threading.Thread.__init__(self)
        self.kill_received = False
        self.ip = ip
        self.port = port
        self.socket = socket
        self.out_q = out_queue
        print "[+] New thread started for " + ip + ":" + str(port) + "."

    def run(self):
        print "Connection from : " + self.ip + ":" + str(self.port)

        data = "dummydata"
        data = self.socket.recv(4096)
        if data not in passwords:
            print "Client " + self.ip + ":" + str(self.port) + " failed to authenticate!"
            self.socket.send("Failed to authenticate.")
            self.shutdown
            return
        else:
            self.socket.send("authenticatesuccess")
            print "Client " + self.ip + ":" + str(self.port) + " authenticated!"
        i = 0
        while len(data):
            data = self.socket.recv(4096)
            self.out_q.put(("Client " + self.ip + ":" + str(self.port) + " sent: ", data))
            i += 1
        print "Client " + self.ip + ":" + str(self.port) + " disconnected (" + str(i) + " messages received)."

    def shutdown(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        print "[-] Thread for " + self.ip + ":" + str(self.port) + " closing."

host = "127.0.0.1"
port = 8080

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

serversock.bind((host, port))
threads = []
q = Queue.Queue()

newthread = AggregateThread(q)
newthread.start()
threads.append(newthread)
try:
    while True:
        serversock.listen(4)
        print "Waiting for incoming connections..."
        (clientsock, (ip, port)) = serversock.accept()
        newthread = ClientThread(ip, port, clientsock, q)
        newthread.start()
        threads.append(newthread)

except KeyboardInterrupt:
    print "\nKill command received!"
    for t in threads:
        t.kill_received = True
        t.shutdown()

for t in threads:
    t.join()
