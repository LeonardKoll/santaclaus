import zmq
import time
import threading

from wecker import *
from rentier import *
from santa import *
from elf import *

zmqContext = zmq.Context.instance()

weckerThread = threading.Thread(target=wecker, args=(zmqContext,), name="wecker")
weckerThread.start()

rentierThreads = []
for iA in range (9):
    rentierThreads += [threading.Thread(target=rentier, args=(zmqContext,"rudolf"+str(iA)), name="rudolf"+str(iA))]
    rentierThreads[-1].start()

elfThreads = []
for iA in range (9):
    elfThreads += [threading.Thread(target=elf, args=(zmqContext,"elfine"+str(iA)), name="elfine"+str(iA))]
    elfThreads[-1].start()

santaThread = threading.Thread(target=santa, args=(zmqContext,), name="santa")
santaThread.start()

consolePublisher = zmqContext.socket(zmq.PUB)
consolePublisher.bind("inproc://console")
print()
print("Willkommen im Santa-Simulator")
print()
while (True):
    consolePublisher.send_string(input())

print("===============================================")
print("stopped.")
zmqContext.term()
