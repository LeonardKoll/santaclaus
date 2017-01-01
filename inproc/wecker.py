import zmq


def wecker(context):

    puller = context.socket(zmq.PULL)
    puller.bind("inproc://weckerAnmeldung")

    pair = context.socket(zmq.PAIR)
    pair.bind("inproc://weckerAlarm")


    anwesendeRentiere     = []
    hilfsbeduerftigeElfen = []

    while(True):

        message = str(puller.recv(),'utf-8').split(' ')
        if   (message[0] == "eingetroffen"):
            anwesendeRentiere += [message[1]]
        elif (message[0] == "abgereist"):
            anwesendeRentiere.remove(message[1])
        elif (message[0] == "hilfegesuch"):
            hilfsbeduerftigeElfen += [message[1]]
        elif (message[0] == "problemgeloest"):
            hilfsbeduerftigeElfen.remove(message[1])

        if   (len(anwesendeRentiere) >= 9):
            pair.send_string("aufwachen! xmas")
        elif (len(hilfsbeduerftigeElfen) >= 3):
            pair.send_string("aufwachen! probleme")
