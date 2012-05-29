__author__ = 'Huang Yung-Tai'


import zmq


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5000")

while True:
    msg = socket.recv()
    if msg not in ("end", "hangup"):
        print "Received", msg
        socket.send(msg)
    else:
        print "Received ", msg, ", Terminating"
        break
