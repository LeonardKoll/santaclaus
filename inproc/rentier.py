import zmq
import time

def rentier(context, name):

    publisher = context.socket(zmq.PUSH)
    publisher.connect("inproc://weckerAnmeldung")
    #time.sleep(1) #Das läuft schief wenn schon welche senden während sich andere noch connecten.

    publisher.send_string("eingetroffen " + name)
