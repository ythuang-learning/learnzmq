__author__ = 'Huang Yung-Tai'

import zmq
import msgpack

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5000")

while True:
    serialized = socket.recv()
    msg = msgpack.unpackb(serialized)
    if msg not in ("end", "hangup"):
        print "Received", msg
        socket.send(msgpack.packb(msg))
    else:
        print "Received ", msg, ", Terminating"
        break
