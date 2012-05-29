__author__ = 'Huang Yung-Tai'


import zmq


context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5000")

for i in range(10):
    msg = "msg %s" % i
    socket.send(msg)
    print "Sending ", msg
    reply = socket.recv()
    print "Reply ", reply

socket.send("end")