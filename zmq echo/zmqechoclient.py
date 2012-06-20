__author__ = 'Huang Yung-Tai'

import zmq
import msgpack

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5000")

def get_msg(msg):
    return msgpack.packb(msg)

for i in range(10):
    serialized = msgpack.packb("msg %s" % i)
    socket.send(serialized)
    #print "Sending ", msg
    reply = socket.recv()
    deserialized = msgpack.unpackb(reply)
    print "Reply ", deserialized

serialized = msgpack.packb("end")
socket.send(serialized)