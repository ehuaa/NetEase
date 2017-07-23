import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = socket.gethostname()
port = 5002
s.connect((host, port))

tm = s.recv(1024)

print ("Sai is : %s" % tm.decode('ascii'))