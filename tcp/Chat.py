import zmq

# Message(requestID, instruction, sudoku) und uebergeben
# Versendet Informationen als ZMQ Multipart.
# zmqPORT ist der Port, auf dem Camel empfaengt

zmqContext = zmq.Context.instance()
zmqSocket = zmqContext.socket(zmq.REP)
zmqSocket.bind("tcp://*:5555")
print("Ready.")

while(True):
    print(str(zmqSocket.recv()))
    zmqSocket.send_string(raw_input())
