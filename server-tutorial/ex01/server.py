import socket
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
print repr(host)

port = 5002
serversocket.bind((host, port))
serversocket.listen(5)

while True:
    try:
        clientsocket,addr=serversocket.accept()
    except:
        print "error"

#    print("Got a connection from %s" % str(addr))
#    currentTime = "This message is from sai"
#    clientsocket.send(currentTime.encode('ascii'))
#    clientsocket.close();
