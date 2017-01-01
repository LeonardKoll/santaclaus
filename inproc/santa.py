import zmq


def santa(context):

    pair = context.socket(zmq.PAIR)
    pair.connect("inproc://weckerAlarm")

    publisher = context.socket(zmq.PUB)
    publisher.bind("inproc://santaSag")

    router = context.socket(zmq.ROUTER)
    router.bind("inproc://elfenTalk")

    ###########################################################################

    console = context.socket(zmq.SUB)
    console.connect("inproc://console")
    console.subscribe("santa")

    poller = zmq.Poller()
    poller.register(subscriber, zmq.POLLIN)
    poller.register(console, zmq.POLLIN)
    poller.register(router, zmq.POLLIN)

    ###########################################################################

    istWach = False

    while(True):

        socks = dict(poller.poll())
        message=""
        if pair in socks and socks[pair] == zmq.POLLIN:
            message = str(pair.recv(),'utf-8').split(' ')
        elif console in socks and socks[console] == zmq.POLLIN:
            message = str(console.recv(),'utf-8').split(' ')

            if   (message[1] == "sag"):
                toSend = ' '.join(message[2:-1])
                publisher.send_string(toSend)
            elif (message[1] == "aufwachen!")
                istWach = True
                console.subscribe("santa")
                if  (message[2] == "xmas"):
                    publisher.send_string("rentiere einspannen")
                    publisher.send_string("rentiere zisch") # loslaufen
                    publisher.send_string("rentiere zisch") # stehenbleiben
                    publisher.send_string("rentiere ausspannen")
                    publisher.send_string("rentiere zisch") # Karibik
                elif (message[2] = "probleme"):
                    publisher.send_string("elfen werbrauchthilfe?")
            elif (message[1] == "einschlafen"):
                istWach = False                     # wenn santa schläft ...
                subscriber.unsubscribe("santa")     # ... kann er auch nicht zuhören

        elif router in socks and socks[router] == zmq.POLLIN:
            # Elfentalk Kommunikation muss hier wg den Eigenheiten des ROUTER Sockets separat gehandhabt werden.
            address, empty, message = router.recv_multipart()
            senderSocket.send_multipart([address,b'',b'dummenuss machsanders'])
            # dummenuss steht hier, damit beim elf das 'machsanders' in message[1] steht.
            # Andernfalls muesste man die elfenTalk Kommunikation separat handahaben (Aufwand)
