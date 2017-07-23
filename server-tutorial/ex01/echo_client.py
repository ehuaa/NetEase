import socket

host=socket.gethostname()
port = 12345

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
for i in xrange(10):
    s.sendall(repr(i))
    data=s.recv(1024)
    print data

s.close()

