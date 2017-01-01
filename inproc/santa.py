import zmq
import time
import threading



class Santa (threading.Thread):

    def __init__(self, context, anzElfen):

        threading.Thread.__init__(self)

        self.pair = context.socket(zmq.PAIR)
        self.publisher = context.socket(zmq.PUB)
        self.router = context.socket(zmq.ROUTER)

        self.istWach = False
        self.anzElfen = anzElfen
        self.elfenAnswers = anzElfen


    def _configure_ (self):

        self.pair.connect("inproc://weckerAlarm")
        self.publisher.bind("inproc://santaSag")
        self.router.bind("inproc://elfenTalk")

        self.poller = zmq.Poller()
        self.poller.register(self.pair, zmq.POLLIN)
        self.poller.register(self.router, zmq.POLLIN)

    def _geschenkeAusliefern_(self):
        print("Santa: Ich liefere jetzt Geschenke aus.")
        self.publisher.send_string("rentiere einspannen")
        time.sleep(0.1)
        self.publisher.send_string("rentiere zisch") # loslaufen
        time.sleep(0.1)
        self.publisher.send_string("rentiere zisch") # stehenbleiben
        time.sleep(0.1)
        self.publisher.send_string("rentiere ausspannen")
        time.sleep(0.1)
        self.publisher.send_string("rentiere zisch") # Karibik
        time.sleep(0.1)
        print("Santa: Ich bin fertig mit Ausliefern.")

    def _aufwachen_(self):
        if (not self.istWach):
            print("Santa: Ich bin aufgewacht.")
            self.istWach = True

    def _einschlafen_(self):
        if (self.istWach):
            print("Santa: Ich gehe jetzt schlafen.")
            self.istWach = False

    def run(self):

        self._configure_()

        while(True):

            socks = dict(self.poller.poll())
            message=[]
            if self.pair in socks and socks[self.pair] == zmq.POLLIN:
                message = str(self.pair.recv(),'utf-8').split(' ')

                if (message[1] == "aufwachen" and not self.istWach):
                    self._aufwachen_()
                    if  (message[2] == "xmas"):
                        self._geschenkeAusliefern_()
                        self._einschlafen_()
                    elif (message[2] == "probleme" and self.elfenAnswers == self.anzElfen):
                        print("Santa: Wer braucht hilfe?")
                        self.publisher.send_string("elfen werbrauchthilfe?")
                        self.elfenAnswers = 0

            elif self.router in socks and socks[self.router] == zmq.POLLIN:
                address, empty, message = self.router.recv_multipart()
                message = str(message,'utf-8').split(' ')

                if   (message[0] == "ichbrauchhilfe"):
                    print("Santa: Ich helfe " + message[1])
                    self.router.send_multipart([address,b'',b'machsanders'])
                    self.elfenAnswers += 1
                elif (message[0] == "ichnicht"):
                    self.router.send_multipart([address,b'',b'ok'])
                    self.elfenAnswers += 1

            if (self.elfenAnswers >= self.anzElfen):
                self._einschlafen_()
