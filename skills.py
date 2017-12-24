from bus import Payload, Slave
import settings as setti

bus=None
bus2=None

def handleUtterance(payload):
    p=Payload('recognizer_loop:utterance',payload.data,payload.context)
    print(str(p))
    bus2.emit(p)
#    payload=Payload('speak',{'text':payload.data['utterances'][0]})
#    bus.emit(payload)

def main():
    global bus, bus2
    bus=Slave()
    bus2=Slave('192.168.1.106')
    bus.on('handleUtterance',handleUtterance)
    bus.listen()

if __name__=='__main__':
    main()
