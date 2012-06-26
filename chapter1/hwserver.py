import zmq
import time
import msgpack

ctx = zmq.Context()

socket = ctx.socket(zmq.REP)

socket.bind("tcp://*:5555")

dowork = True
while dowork:
    msg = msgpack.unpackb(socket.recv())
    #print "message length: ", len(msg), "message:", msg
    msglen = len(msg)
    if msglen == 3:
        #print "Received message %d [%s] from client %d" %(msg[2], msg[1], msg[0])
        #time.sleep(1)
        reply_msg = msgpack.packb("World")
        socket.send(reply_msg)
    elif msglen == 1:
        dowork = False

socket.close()
