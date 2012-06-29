#!/usr/bin/env python

import zmq
import time
import msgpack

ctx = zmq.Context()

socket = ctx.socket(zmq.REP)

socket.bind("tcp://*:5555")

do_work = True
while do_work:
    msg = msgpack.unpackb(socket.recv())

    print "Received: Client %d sent message #%d with text:[%s] " % ( msg['id'], msg['req_id'], msg['msg'])
    if msg['msg'] == "Bye":
        do_work = False
    msg['msg'] = "World"
    socket.send(msgpack.packb(msg))

socket.close()
