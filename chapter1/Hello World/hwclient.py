#!/usr/bin/env python

from gevent_zeromq import zmq
import gevent
import time
import msgpack
import random

ctx = zmq.Context()


def sleep():
    sleep_interval = random.random() * 3
    print "sleeping ", sleep_interval
    time.sleep(sleep_interval)


def client_send(id):
    socket = ctx.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    #sleep()
    for request in range(1, 1001):
        print "Client %d Sending request %s ... " % (id, request)
        msg = {"id": id, "msg": "Hello", "req_id": request}
        socket.send(msgpack.packb(msg))
        #sleep()
        reply_msg = msgpack.unpackb(socket.recv())
        print "Reply: Client %d Received reply %d: %s" % (reply_msg['id'], reply_msg['req_id'], reply_msg['msg'])

    socket.close()

start_time = time.time()
threads = [gevent.spawn(client_send, i) for i in range(1, 11)]
gevent.joinall(threads)
end_time = time.time()
elapsed = end_time - start_time

print "sending end message"
end_socket = ctx.socket(zmq.REQ)
end_socket.connect("tcp://localhost:5555")
end_msg = {"id": 0, "msg": "Bye", "req_id": 0}
end_socket.send(msgpack.packb(end_msg))
reply_msg = msgpack.unpackb(end_socket.recv())
end_socket.close()
print "sent end message"
print "Time taken: ", elapsed
print "Msg/s: ", 10000/elapsed
