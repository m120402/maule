import socket


# Tutorial came from:
# https://pythonprogramming.net/sockets-tutorial-python-3/

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Now, since this is the client, rather than binding, we are going to connect.
s.connect((socket.gethostname(), 1234))

# In the more traditional sense of client and server, 
# you wouldnt actually have the client and server on the same machine.
# If you wanted to have two programs talking to eachother locally, 
# you could do this, but typically your client will more likely connect 
# to some external server, using its public IP address, 
# not socket.gethostname(). You will pass the string of the IP instead.


# So we've sent some data, now we want to receive it.
# The Server sent "Hey There!!!"

msg = s.recv(1024)

# This means our socket is going to attempt to receive data, 
# in a buffer size of 1024 bytes at a time.

# Then, let's just do something basic with the data we get, 
# like print it out!

print(msg.decode("utf-8"))



