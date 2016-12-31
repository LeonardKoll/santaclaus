import zmq
import time
import threading

from wecker import *
from rentier import *
from santa import *

zmqContext = zmq.Context.instance()

weckerThread = threading.Thread(target=wecker, args=(zmqContext,))
weckerThread.start()

time.sleep(0.5)

rentierThreads = []
for iA in range (9):
    rentierThreads += [threading.Thread(target=rentier, args=(zmqContext,"Rudolf"+str(iA)))]
    rentierThreads[-1].start()

time.sleep(0.5)

santaThread = threading.Thread(target=santa, args=(zmqContext,))
santaThread.start()


time.sleep(5)
zmqContext.term()
print("stopped.")
