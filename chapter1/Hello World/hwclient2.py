#!/usr/bin/env python

from gevent_zeromq import zmq
import gevent
import time
import msgpack
import random

ctx = zmq.Context()


def send_message(count, id = 1):
    socket = ctx.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    #sleep()
    for request in range(1, count):
        #print "Client %d Sending request %s ... " % (id,request)
        msg = [id, "hello", count]
        socket.send(msgpack.packb(msg))
        #sleep()
        reply_msg =msgpack.unpackb(socket.recv())
        #print "Client %d Received reply %d: %s" % (id, request, reply_msg)
    socket.close()
c = 10000
start_time = time.time()
send_message(c)



print "sending end message"
end_socket = ctx.socket(zmq.REQ)
end_socket.connect("tcp://localhost:5555")
end_msg = msgpack.packb(['end'])
end_socket.send(end_msg)
time.sleep(0.1)
end_socket.close()
print "sent end message"
end_time = time.time()

print "started: ",start_time, " ended: ", end_time
diff = end_time - start_time
print "lasted :", diff
print c/diff, "msg/s"