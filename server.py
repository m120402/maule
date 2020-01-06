import socket

# Tutorial came from:
# https://pythonprogramming.net/sockets-tutorial-python-3/

# create the socket
# AF_INET == ipv4
# SOCK_STREAM == TCP


# The s variable is our TCP/IP socket. 
# The AF_INET is in reference to th family or domain, it means ipv4, as opposed to ipv6 with AF_INET6. 
# The SOCK_STREAM means it will be a TCP socket, which is our type of socket. 
# TCP means it will be connection-oriented, as opposed to connectionless.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# A socket will be tied to some port on some host. 
# In general, you will have either a client or a server type of entity or program.

# In the case of the server, you will bind a socket to some port on the server (localhost). 
# In the case of a client, you will connect a socket to that server, on the same port that the server-side code is using.

# For IP sockets, the address that we bind to is a tuple of the hostname and the port number.
s.bind((socket.gethostname(), 1234))


# Now that we've done that, let's listen for incoming connections. 
# We can only handle one connection at a given time, so we want to allow for some sort of a queue, just incase we get a slight burst. 
# If someone attempts to connect while the queue is full, they will be denied.
# Let's make a queue of 5
s.listen(5)


# And now, we just listen!
while True:
	# now our endpoint knows about the OTHER endpoint.
	clientsocket, address = s.accept()
	print(f"Connection from {address} has been established.")

# So we've made a connection, and that's cool, but we really want to 
# send messages and/or data back and forth. How do we do that?

# Our sockets can send and recv data. These methods of handling data 
# deal in buffers. Buffers happen in chunks of data of some fixed size. 
# Let's see that in action:
	clientsocket.send(bytes("Hey there!!!","utf-8"))