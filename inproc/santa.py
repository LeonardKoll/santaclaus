import zmq


def santa(context):

    pair = context.socket(zmq.PAIR)
    pair.connect("inproc://weckerAlarm")

    publisher = context.socket(zmq.PUSH)
    publisher.bind("inproc://santaSag")

    while(True):

        message = str(pair.recv(),'utf-8')
        print(message)
