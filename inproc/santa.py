import zmq


def santa(context):

    pair = context.socket(zmq.PAIR)
    pair.connect("inproc://weckerAlarm")

    while(True):

        message = str(pair.recv(),'utf-8')
        print(message)
