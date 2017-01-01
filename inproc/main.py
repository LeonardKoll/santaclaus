import zmq
import time
import threading

from wecker import *
from rentier import *
from santa import *

zmqContext = zmq.Context.instance()

weckerThread = threading.Thread(target=wecker, args=(zmqContext,))
weckerThread.start()

rentierThreads = []
for iA in range (9):
    rentierThreads += [threading.Thread(target=rentier, args=(zmqContext,"Rudolf"+str(iA)))]
    rentierThreads[-1].start()

santaThread = threading.Thread(target=santa, args=(zmqContext,))
santaThread.start()

consolePublisher = zmqContext.socket(zmq.PUB)
consolePublisher.bind("inproc://console")
print()
print("Willkommen im Santa-Simulator")
print()
while (True):
    consolePublisher.send_string(input())


time.sleep(5)
zmqContext.term()
print("stopped.")
