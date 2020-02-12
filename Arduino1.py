import serial, random, time

port = "COM1"
ser = serial.Serial(port, 9600)

while (True): 
	s1=random.randint(15, 50)
	s2=random.randint(15, 100)
	

	m1 = str(s1)
	m1 += "\r\n"

	m2 = str(s2)
	m2 += "\r\n"

	ser.write(m1.encode())
	ser.write(m2.encode())


	print("s1 es", s1)
	print("s2 es", s2)

	time.sleep(1)
ser.close()
