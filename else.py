def desired_input(mutex,T_in,fileno):
	sys.stdin = os.fdopen(fileno)
	while(True):
		mutex.acquire()
		try:
			s = input('Please enter the desired Temperature: ')
		except:
			s = 0
		T_in.Value = float(s)
		T_in.value = float(s)
		print T_in.Value
		print T_in.value
		mutex.release()