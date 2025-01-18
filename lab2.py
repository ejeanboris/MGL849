import thread
import time
import threading
from threading import Lock
from multiprocessing import Process, Value
import socket
import sys, os
import re

serverName = 'compaq'

#Variables
G1 = 0
mutex_g1 = Lock()
G2 = 0
mutex_g2 = Lock()
G3 = 0
mutex_g3 = Lock()

alarm = 'AG1\nAG2\nAG3\n'
mutex_alarm = Lock()
aeration = 'AN\n'
mutex_aeration = Lock()
ventilation = 'VN\n'
mutex_ventilation = Lock()
injection = 'AIG1\nAIG2\nAIG3\n'
mutex_injection = Lock()


def reader():
	global G1
	global mutex_g1
	global G2
	global mutex_g2
	global G3
	global mutex_g3
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((serverName, 1231))
	# Receive the data in small chunks and retransmit it
	print('Connection Etablie')
	while (True):
		raw = sock.recv(1024)
		data = re.search('^(LG\d)(\d+)',raw)
		if(data.group(1) == 'LG1'): 
			mutex_g1.acquire()
			G1 = int(data.group(2))
			mutex_g1.release()
		if(data.group(1) == 'LG2'): 
			mutex_g2.acquire()
			G2 = int(data.group(2))
			mutex_g2.release()
		if(data.group(1) == 'LG3'): 
			mutex_g3.acquire()
			G3 = int(data.group(2))
			print(G3)
			mutex_g3.release()
		
	sock.close()
	
	
def sender():
	global alarm
	global mutex_alarm
	global aeration
	global mutex_aeration
	global ventilation
	global mutex_ventilation
	global injection
	global mutex_injection
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((serverName, 1232))
	# Receive the data in small chunks and retransmit it
	print('Connection Etablie')
	while (True):
		mutex_alarm.acquire()
		sock.send(alarm)
		mutex_alarm.release()
		
		mutex_aeration.acquire()
		sock.send(aeration)
		mutex_aeration.release()
		
		mutex_ventilation.acquire()
		sock.send(ventilation)
		mutex_ventilation.release()
		
		mutex_injection.acquire()
		sock.send(injection)
		mutex_injection.release()
	sock.close()



def reponse():
	global G1
	global mutex_g1
	global G2
	global mutex_g2
	global G3
	global mutex_g3
	
	global alarm
	global mutex_alarm
	global aeration
	global mutex_aeration
	global ventilation
	global mutex_ventilation
	global injection
	global mutex_injection

	while(True):
		mutex_g1.acquire()
		cg1 = G1
		mutex_g1.release()
		mutex_g2.acquire()
		cg2 = G2
		mutex_g2.release()
		mutex_g3.acquire()
		cg3 = G3
		mutex_g3.release()
		
		if(cg1>50 and cg2>50 and cg3>50):
			mutex_aeration.acquire()
			aeration = 'AL1\n'
			mutex_aeration.release()
			
			mutex_ventilation.acquire()
			ventilation = 'VL2\n'
			mutex_ventilation.release()
			print('state 1')
		
		elif(cg1>21 and cg2>21 and cg3>21):
			
			mutex_aeration.acquire()
			aeration = 'AL2\n'
			mutex_aeration.release()
			
			mutex_ventilation.acquire()
			ventilation = 'VL1\n'
			mutex_ventilation.release()
			print('state 2')
		
		
		elif(cg1>5 and cg2>5 and cg3>5):
			mutex_aeration.acquire()
			aeration = 'AL2\n'
			mutex_aeration.release()
			
			mutex_ventilation.acquire()
			ventilation = 'VN\n'
			mutex_ventilation.release()
			print('state 3')
			
		
		elif(cg1>1 and cg2>1 and cg3>1):
			mutex_aeration.acquire()
			aeration = 'AN\n'
			mutex_aeration.release()
			
			mutex_ventilation.acquire()
			ventilation = 'VN\n'
			mutex_ventilation.release()
			print('state 4')
		
	
		if(cg1>45):
			mutex_injection.acquire()
			injection += 'IG1\n'
			mutex_injection.release()
			mutex_alarm.acquire()
			alarm += 'AG1H\n'
			mutex_alarm.release()
		elif(cg1>30):
			mutex_injection.acquire()
			injection += 'IG1\n'
			mutex_injection.release()
			mutex_alarm.acquire()
			alarm += 'AG1M\n'
			mutex_alarm.release()
		elif(cg1>15):
			mutex_injection.acquire()
			injection += 'AIG1\n'
			mutex_injection.release()
			mutex_alarm.acquire()
			alarm += 'AG1L\n'
			mutex_alarm.release()
		
		
		if(cg2>45):
			mutex_injection.acquire()
			injection += 'IG2\n'
			mutex_injection.release()
			mutex_alarm.acquire()
			alarm = 'AG2H\n'
			mutex_alarm.release()
		elif(cg2>30):
			mutex_injection.acquire()
			injection += 'IG2\n'
			mutex_injection.release()
			mutex_alarm.acquire()
			alarm += 'AG2M\n'
			mutex_alarm.release()
		elif(cg2>15):
			mutex_injection.acquire()
			injection += 'AIG2\n'
			mutex_injection.release()
			mutex_alarm.acquire()
			alarm += 'AG2L\n'
			mutex_alarm.release()
		
		
		
		if(cg3>45):
			mutex_injection.acquire()
			injection += 'IG3\n'
			mutex_injection.release()
			mutex_alarm.acquire()
			alarm += 'AG3H\n'
			mutex_alarm.release()
		elif(cg3>30):
			mutex_injection.acquire()
			injection += 'IG3\n'
			mutex_injection.release()
			mutex_alarm.acquire()
			alarm += 'AG3M\n'
			mutex_alarm.release()
		elif(cg3>15):
			mutex_injection.acquire()
			injection += 'AIG3\n'
			mutex_injection.release()
			mutex_alarm.acquire()
			alarm += 'AG3L\n'
			mutex_alarm.release()
		



	
def main():
	print ('init')
	###Variables

	
	p_reader = threading.Thread(target=reader,args=())
	p_sender = threading.Thread(target=sender,args=())
	p_reponse = threading.Thread(target=reponse,args=())
	p_reader.start()
	p_sender.start()
	p_reponse.start()
	
	#time.sleep(10000)
	print ('done')

if __name__ == '__main__':
	main()
