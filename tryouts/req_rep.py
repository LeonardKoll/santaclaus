import threading
import zmq
import time

def replier (context):
    senderSocket = context.socket(zmq.REP)
    #senderSocket.bind("tcp://*:5555")
    senderSocket.bind("inproc://meinKanal")
    print(senderSocket.recv())

def requester (context):
    recvSocket = context.socket(zmq.REQ)
    #recvSocket.connect("tcp://localhost:5555")
    recvSocket.connect("inproc://meinKanal")
    recvSocket.send_string("Hello World")

zmqContext = zmq.Context.instance()

sThread = threading.Thread(target=replier, args=(zmqContext,))
sThread.start()
time.sleep(1)
rThread = threading.Thread(target=requester, args=(zmqContext,))
rThread.start()

time.sleep(3)

zmqContext.term()

print("stopped.")
