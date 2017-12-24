from bus import Slave, Payload

s=Slave('192.168.1.106')

s.emit(Payload('recognizer_loop:utterance',{'utterances':['hello world']}))
s.close()
