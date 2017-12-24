from bus import Slave, Payload
import settings as setti
import subprocess

def speak(payload):
    data=payload.data
    
    proc=subprocess.Popen([setti.TTSPATH,"-voice","kal16","-t",data["utterance"]])
    proc.communicate()

def main():
    
    bus=Slave()
    bus.on("speak",speak)
    bus.listen()

if __name__ == "__main__":
    main()
