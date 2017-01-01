import zmq

def elf(context, name):

    publisher = context.socket(zmq.PUSH)
    publisher.connect("inproc://weckerAnmeldung")

    subscriber = context.socket(zmq.SUB)
    subscriber.connect("inproc://santaSag")
    subscriber.subscribe(name)          # Rentier hört auf seinen Namen
    subscriber.subscribe("elfen")    # ... und alternativ auf "elfen"

    ###########################################################################

    console = context.socket(zmq.SUB)
    console.connect("inproc://console")
    console.subscribe(name)
    console.subscribe("elfen")

    poller = zmq.Poller()
    poller.register(subscriber, zmq.POLLIN)
    poller.register(console, zmq.POLLIN)

    ###########################################################################

    hatProblem = False

    while (True):

        socks = dict(poller.poll())
        if subscriber in socks and socks[subscriber] == zmq.POLLIN:

            message = str(subscriber.recv(),'utf-8').split(' ')
            if (message[1] == "machsanders"):
                hatProblem = False
                publisher.send_string("problemgeloest " + name)

        if console in socks and socks[console] == zmq.POLLIN:

            message = str(console.recv(),'utf-8').split(' ')
            if   (message[1] == "problem"):
                hatProblem = True
                publisher.send_string("hilfegesuch " + name)
            elif (message[1] == "arbeite"):
                hatProblem = False
                publisher.send_string("problemgeloest " + name)
