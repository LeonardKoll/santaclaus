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
            print("Wecker: riiiiiiiiiiing; Weihnachten")
            pair.send_string("schnarchnase aufwachen xmas")
            # schnarchnase steht hier, damit beim santa das 'aufwachen!' in message[1] steht.
        elif (len(hilfsbeduerftigeElfen) >= 3):
            print("Wecker: riiiiiiiiiiing; Probleme")
            pair.send_string("schnarchnase aufwachen probleme")
