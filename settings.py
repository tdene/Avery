import socket

TTSPATH="flite"
models=['resources/Hello_Avery.pmdl','resources/Hey_Avery.pmdl']
COMPORT=8990
def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ret=s.getsockname()[0]
    s.close()
    return ret
