from gevent_zeromq import zmq
import gevent
import time
import msgpack
import random

ctx = zmq.Context()


def sleep():
    sleepinterval = random.random() * 3
    print "sleeping ", sleepinterval
    time.sleep(sleepinterval)


def client_send(id):
    socket = ctx.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    msg = [id, "hello"]
    #sleep()
    for request in range(1, 10):
        print "Client %d Sending request %s ... " % (id,request)
        socket.send(msgpack.packb(msg))
        #sleep()
        reply_msg =msgpack.unpackb(socket.recv())
        print "Client %d Received reply %d: %s" % (id, request, reply_msg)
    socket.close()
print time.ctime()
threads = [gevent.spawn(client_send,i) for i in range(1,10)]
gevent.joinall(threads)


print "sending end message"
end_socket = ctx.socket(zmq.REQ)
end_socket.connect("tcp://localhost:5555")
end_msg = msgpack.packb(['end'])
end_socket.send(end_msg)
time.sleep(0.1)
end_socket.close()
print "sent end message"
print time.ctime()