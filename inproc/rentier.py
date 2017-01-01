import zmq
import time

def rentier(context, name):

    publisher = context.socket(zmq.PUSH)
    publisher.connect("inproc://weckerAnmeldung")

    subscriber = context.socket(zmq.SUB)
    subscriber.connect("inproc://rentierOrders")
    subscriber.subscribe(name)          # Rentier hört auf seinen Namen
    subscriber.subscribe("rentiere")    # ... und alternativ auf "rentiere"

    ###########################################################################

    console = context.socket(zmq.SUB)
    console.connect("inproc://console")
    console.subscribe(name)
    console.subscribe("rentiere")

    poller = zmq.Poller()
    poller.register(subscriber, zmq.POLLIN)
    poller.register(console, zmq.POLLIN)

    ###########################################################################

    eingespannt = False
    amLaufen    = False
    imUrlaub    = True

    while (True):

        socks = dict(poller.poll())
        if subscriber in socks and socks[subscriber] == zmq.POLLIN:

            message = str(subscriber.recv(),'utf-8').split(' ')
            if   (message[1] == "einspannen"):
                eingespannt = True
            elif (message[1] == "ausspannen"):
                eingespannt = False
                amLaufen    = False
            elif (message[1] == "Zisch"):
                # Wenn eingespannt: Wechsel zwischen stehen und laufen;
                # Wenn ausgespannt: Ab in den Urlaub!
                if (eingespannt):
                    amLaufen = not amLaufen
                else:
                    amLaufen = False
                    imUrlaub = True

        if console in socks and socks[console] == zmq.POLLIN:
            message = str(console.recv(),'utf-8').split(' ')
            if   (message[1] == "home"):
                imUrlaub = False
                publisher.send_string("eingetroffen " + name)
            elif (message[1] == "holiday"):
                imUrlaub = True
                publisher.send_string("abgereist " + name)
