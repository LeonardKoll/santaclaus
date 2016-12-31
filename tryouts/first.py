import threading
import zmq
import time

def sender (context):
    senderSocket = context.socket(zmq.PAIR)
    #senderSocket.bind("tcp://*:5555")
    senderSocket.bind("inproc://meinKanal")
    senderSocket.send_string("Hello World")

def receiver (context):
    recvSocket = context.socket(zmq.PAIR)
    #recvSocket.connect("tcp://localhost:5555")
    recvSocket.connect("inproc://meinKanal")
    print(recvSocket.recv())

zmqContext = zmq.Context.instance()

sThread = threading.Thread(target=sender, args=(zmqContext,))
sThread.start()
rThread = threading.Thread(target=receiver, args=(zmqContext,))
rThread.start()

time.sleep(3)

zmqContext.term()

print("stopped.")
