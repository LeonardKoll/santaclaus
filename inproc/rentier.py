import zmq
import threading



class Rentier (threading.Thread):

    def __init__ (self, context, name):

        threading.Thread.__init__(self)

        self.name = name
        self.publisher = context.socket(zmq.PUSH)
        self.subscriber = context.socket(zmq.SUB)
        self.console = context.socket(zmq.SUB)

        self.eingespannt = False
        self.amLaufen    = False
        self.imUrlaub    = True

    def _configure_(self):

        self.publisher.connect("inproc://weckerAnmeldung")
        self.subscriber.connect("inproc://santaSag")
        self.console.connect("inproc://console")

        self.console.subscribe(self.name)
        self.console.subscribe("rentiere")
        #self.subscriber.subscribe(name)          # Rentier hört auf seinen Namen
        #self.subscriber.subscribe("rentiere")    # ... und alternativ auf "rentiere"
                                             # aber erst wenn sie am Pol sind.
        self.poller = zmq.Poller()
        self.poller.register(self.subscriber, zmq.POLLIN)
        self.poller.register(self.console, zmq.POLLIN)

    def _goHoliday_(self):
        print(self.name + ": Ich geh in die Karibik.")
        self.amLaufen = False
        self.imUrlaub = True
        self.publisher.send_string("abgereist " + self.name)
        # nicht mehr in Hoerweite
        self.subscriber.unsubscribe(self.name)          # Rentier hört auf seinen Namen
        self.subscriber.unsubscribe("rentiere")    # ... und alternativ auf "rentiere"

    def run(self):

        self._configure_()

        while (True):

            socks = dict(self.poller.poll())
            message = []
            if self.subscriber in socks and socks[self.subscriber] == zmq.POLLIN:
                message = str(self.subscriber.recv(),'utf-8').split(' ')

                if   (message[1] == "einspannen"):
                    self.eingespannt = True
                    print(self.name + ": Ich bin eingespannt.")
                elif (message[1] == "ausspannen"):
                    self.eingespannt = False
                    self.amLaufen    = False
                    print(self.name + ": Ich bin ausgespannt.")
                elif (message[1] == "zisch"):
                    # Wenn eingespannt: Wechsel zwischen stehen und laufen;
                    # Wenn ausgespannt: Ab in den Urlaub!
                    if (self.eingespannt):
                        self.amLaufen = not self.amLaufen
                        print(self.name + ": amLaufen = " + str(self.amLaufen))
                    else:
                        self._goHoliday_()

            elif self.console in socks and socks[self.console] == zmq.POLLIN:
                message = str(self.console.recv(),'utf-8').split(' ')

                if   (message[1] == "home"):
                    print(self.name + ": Ich treffe am Pol ein.")
                    self.imUrlaub = False
                    self.publisher.send_string("eingetroffen " + self.name)
                    # wieder in Hoerweite
                    self.subscriber.subscribe(self.name)          # Rentier hört auf seinen Namen
                    self.subscriber.subscribe("rentiere")    # ... und alternativ auf "rentiere"
                elif (message[1] == "holiday"):
                    self._goHoliday_()
