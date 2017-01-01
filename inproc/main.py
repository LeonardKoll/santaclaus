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

santaThread = Santa(zmqContext, 12)
santaThread.start()

rentierThreads = []
for iA in range (9):
    rentierThreads += [Rentier(zmqContext, "rudolf"+str(iA))]
    rentierThreads[-1].start()

elfThreads = []
for iA in range (12):
    elfThreads += [Elf(zmqContext, "elfine"+str(iA))]
    elfThreads[-1].start()

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
