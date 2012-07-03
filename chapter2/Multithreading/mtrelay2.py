"""

   Multithreaded relay

   Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>

"""

import threading
import zmq
import time


def step(context, chain_depth, max_chain_depth):
    """ stepping """

    #url = "inproc://step%s"
    url = "ipc://step%s"

    if chain_depth < max_chain_depth:
        # Bind to inproc: endpoint, then start upstream thread
        receiver = context.socket(zmq.PAIR)
        receiver.bind(url % (chain_depth + 1))

        thread = threading.Thread(target=step, args=(context, chain_depth + 1, max_chain_depth ))
        thread.start()
        # Wait for signal
        string = receiver.recv()
        print "Got ack at depth %03d message: %s" % (chain_depth, string)
        if not chain_depth:
            print("Test successful!\n")
        time.sleep(0.1)
        receiver.close()


    if chain_depth > 0:
        # Signal downstream
        sender = context.socket(zmq.PAIR)
        sender.connect(url % chain_depth)
        msg = "OK from %03d " % chain_depth
        sender.send(msg)

    return


def main():
    """ server routine """
    # Prepare our context and sockets
    context = zmq.Context(1)

    max_depth = 100
    depth = 0

    step(context, depth, max_depth)

    context.term()

    return

if __name__ == "__main__":
    main()