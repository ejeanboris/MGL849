import thread
import time
from threading import Lock
from multiprocessing import Process, Value
import socket
import sys, os



def reader(mutex,T_red,Pr,Hd):
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(('MAIN', 1231))
	# Receive the data in small chunks and retransmit it
	while (True):
		mutex.acquire()
		raw = sock.recv(4096)
		mutex.release()
		print(raw)
		time.sleep(0.5)
		
	sock.close()
	
	
def sender(mutex,T_in,T_red,Pr,Hd):
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(('MAIN', 1232))
	# Receive the data in small chunks and retransmit it
	while (True):
		mutex.acquire()
		sock.send('AL1')
		mutex.release()
		print(raw)
		time.sleep(0.5)
		
	sock.close()





if __name__ == '__main__':
	###HERE IS THE MAIN
	T_in = Value('d',25.0)
	T_red = Value('d',15.0)
	Pr = Value('d',0.0)
	Hd = Value('d',0.0)

	mutex = Lock()
	print 'init'

	fn = sys.stdin.fileno() #Get the input descriptor to pass to children process

	p_reader = Process(target=reader,args=(mutex,T_red,Pr,Hd))
	p_sender = Process(target=sender,args=(mutex,T_in,T_red,Pr,Hd))
	#p_desiredInput = Process(target=desired_input,args=(mutex,T_in,fn))
	p_reader.start()
	p_sender.start()
	p_desiredInput.start()

	time.sleep(10000)
	print 'done'


