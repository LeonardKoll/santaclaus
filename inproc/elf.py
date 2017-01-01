import zmq
import threading

class Elf (threading.Thread):

    def __init__(self, context, name):

        threading.Thread.__init__(self)

        self.name = name
        self.publisher = context.socket(zmq.PUSH)
        self.subscriber = context.socket(zmq.SUB)
        self.requester = context.socket(zmq.REQ)
        self.console = context.socket(zmq.SUB)

        self.hatProblem = False

    def _configure_(self):

        self.publisher.connect("inproc://weckerAnmeldung")
        self.subscriber.connect("inproc://santaSag")
        self.requester.connect("inproc://elfenTalk")
        self.console.connect("inproc://console")

        self.subscriber.subscribe(self.name)          # Elf hört auf seinen Namen
        self.subscriber.subscribe("elfen")       # ... und alternativ auf "elfen"
        self.console.subscribe(self.name)
        self.console.subscribe("elfen")

        self.poller = zmq.Poller()
        self.poller.register(self.subscriber, zmq.POLLIN)
        self.poller.register(self.console, zmq.POLLIN)
        self.poller.register(self.requester, zmq.POLLIN)


    def _problemgeloest_(self):
        self.hatProblem = False
        print(self.name + ": Danke Santa!")
        self.publisher.send_string("problemgeloest " + self.name)


    def run(self):

        self._configure_()

        while (True):

            socks = dict(self.poller.poll())
            message=[]
            if self.subscriber in socks and socks[self.subscriber] == zmq.POLLIN:
                message = str(self.subscriber.recv(),'utf-8').split(' ')

                if (message[1] == "werbrauchthilfe?"):
                    if (self.hatProblem):
                        print(self.name + ": Ich brauche Hilfe!")
                        self.requester.send_string("ichbrauchhilfe " + self.name)
                        # '-> Eigentlich nicht noetig, den Namen der Elfe anzugeben.
                        #     Santa kann sie ueber ihren Socket identifizieren.
                        #     Ist nur fuer die Ausgabe bei Santa
                    else:
                        self.requester.send_string("ichnicht " + self.name)

            elif self.console in socks and socks[self.console] == zmq.POLLIN:
                message = str(self.console.recv(),'utf-8').split(' ')

                if (message[1] == "problem"):
                    self.hatProblem = True
                    print(self.name + ": Ich melde mich beim Wecker weil ich Hilfe brauche.")
                    self.publisher.send_string("hilfegesuch " + self.name)
                elif (message[1] == "arbeite"):
                    self._problemgeloest_()

            elif self.requester in socks and socks[self.requester] == zmq.POLLIN:
                message = str(self.requester.recv(),'utf-8')
                if (message == "machsanders"):
                    self._problemgeloest_()
