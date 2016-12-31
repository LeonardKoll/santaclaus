import threading
import zmq
import time

def server (context):
    senderSocket = context.socket(zmq.PUB)
    #senderSocket.bind("tcp://*:5555")
    senderSocket.bind("inproc://meinKanal")
    for iA in range (5):
        for subscriptionID in range (2):
            senderSocket.send_string(str(subscriptionID) + " Hello" + str(iA))
            time.sleep(0.5)

def client (context):
    recvSocket = context.socket(zmq.SUB)
    #recvSocket.connect("tcp://localhost:5555")
    recvSocket.connect("inproc://meinKanal")
    # recvSocket.subscribe("") # alle Messages
    recvSocket.subscribe("1")  # nur Messages mit ID 1 (Stringmaching am Anfang)
    while(True):
        print(recvSocket.recv())

zmqContext = zmq.Context.instance()

"""
Wir starten absichtlich den server zuerst. Der sendet im 0.5 sekunden Takt nachrichten.
Der client schaltet sich erst nach 1 Sekunde zu, die ersten beiden Hellos verpasst er also.
"""

sThread = threading.Thread(target=server, args=(zmqContext,))
sThread.start()
time.sleep(1)
rThread = threading.Thread(target=client, args=(zmqContext,))
rThread.start()


time.sleep(3)

zmqContext.term()

print("stopped.")
