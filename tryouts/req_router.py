import threading
import zmq
import time

def replier (context):
    senderSocket = context.socket(zmq.ROUTER)
    #senderSocket.bind("tcp://*:5555")
    senderSocket.bind("inproc://meinKanal")
    address, empty, message = senderSocket.recv_multipart()
    print(address, message)
    senderSocket.send_multipart([address,b'',b'This is the workload'])

def requester (context):
    recvSocket = context.socket(zmq.REQ)
    #recvSocket.connect("tcp://localhost:5555")
    recvSocket.connect("inproc://meinKanal")
    recvSocket.send_string("Hello World")
    print(recvSocket.recv_multipart())

zmqContext = zmq.Context.instance()

sThread = threading.Thread(target=replier, args=(zmqContext,))
sThread.start()
time.sleep(1)
rThread1 = threading.Thread(target=requester, args=(zmqContext,))
rThread1.start()
rThread2 = threading.Thread(target=requester, args=(zmqContext,))
rThread2.start()

time.sleep(3)

zmqContext.term()

print("stopped.")
