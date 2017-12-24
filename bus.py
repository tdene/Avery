import json
from collections import defaultdict
from time import sleep
import socket, os
from threading import Thread

import settings as setti

class Payload:
    def __init__(self,name,data=None,context=None):
        self.name=name
        self.data=data
        self.context=context
    def reply(self,name,data,context=None):
        context = context or {}
        for x in self.context:
            if x not in context:
                context[x]=self.context[x]
        return Payload(name,data,context)
    def __str__(self):
        return json.dumps({
            'name':self.name,
            'data':self.data,
            'context':self.context
        })
    @staticmethod
    def fromString(P):
        P=json.loads(P)
        return Payload(P.get('name'),P.get('data'),P.get('context'))
    
class Bus:
    def __init__(self):
        self._events=defaultdict(set)

    def on(self,name,func):
        self._events[name].add(func)
    
    def _emit(self,payload):
        name=payload.name
        funcs=self._events[name]
        
        threaded=True # ALWAYS MULTITHREADED. IS GOOD??
        if threaded:
            threads=[Thread(target=x,args=[payload]) for x in funcs]
            [x.start() for x in threads]
        else:
            [x(payload) for x in funcs]


class Slave(Bus):
    def __init__(self,IP=setti.getIP()):
        super().__init__()

        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((IP,setti.COMPORT))

    def listen(self,threading=False):
        def dowork():
            while True:
                data=self.socket.recv(1024).decode()
                self._emit(Payload.fromString(data))
        if threading:
            Thread(target=dowork,daemon=True).start()
        else:
            dowork()

    def emit(self,payload):
        self.socket.send(str(payload).encode())
        #self._emit(payload)

    def close(self):
        self.socket.close()

class Master:
    def __init__(self):
        self.localsocks=set()

        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socket.bind((setti.getIP(),setti.COMPORT))

    def listen(self):
        def handle_data(data,addr):
            toRemove=set()
            for a in self.localsocks:
                try:
                    a.send(data)
                except Exception as e:
                    print('error',e)
                    print('sock',a)
                    toRemove.add(a)
            for a in toRemove:
                self.localsocks.remove(a)
        def handle_client(sock,addr):
            while True:
                data=sock.recv(1024)
                if not data:
                    break
                handle_data(data,addr)
            sock.close()

        self.socket.listen()
        while True:
            sock, addr = self.socket.accept()
            if addr[0]==setti.getIP():
                self.localsocks.add(sock)
            Thread(target=handle_client,args=(sock,addr)).start()

    def close(self):
        for a in self.localsocks:
            a.close()
        self.socket.close()

def master():
    m=Master()
    try:
        m.listen()
    except KeyboardInterrupt:
        m.close()

if __name__ == '__main__':
    master()
