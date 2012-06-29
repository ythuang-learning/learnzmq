#!/usr/bin/env python

import zmq
import time
import msgpack
import multiprocessing

count = 100

def send_message(id):
    print "starting", id
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    for request in range(1, count):
        print "Client %d Sending request %s ... " % (id, request)
        msg = [id, "hello", count]
        socket.send(msgpack.packb(msg))
        reply_msg = msgpack.unpackb(socket.recv())
        print "Client %d Received reply %d: %s" % (id, request, reply_msg)
    socket.close()

pool = multiprocessing.Pool(10)

start_time = time.time()
pool.map(send_message, [i for i in range(1, 10)])
end_time = time.time()

print "sending end message"
ctx = zmq.Context()
end_socket = ctx.socket(zmq.REQ)
end_socket.connect("tcp://localhost:5555")
end_msg = msgpack.packb(['end'])
end_socket.send(end_msg)
time.sleep(0.1)
end_socket.close()
print "sent end message"

print "started: ", start_time, " ended: ", end_time
diff = end_time - start_time
print "lasted :", diff
print c / diff, "msg/s"