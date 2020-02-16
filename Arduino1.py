import serial, random, time

port = "COM1"
ser = serial.Serial(port, 9600)

ser.flushInput()
ser.flushOutput()

aux1=random.randint(400, 1200)
aux2=random.randint(400, 1200)

limInf = 0
limSup = 0

#Para generar aleatorios con distinta SD
if(aux1<aux2):
	limInf = aux1
	limSup = aux2
else:
	limInf = aux2
	limSup = aux1
	
time.sleep(3)

while (True): 
	
	#HR beats/min
	s1=random.randint(50, 140)
	
	#RR miliseconds
	s2=random.randint(limInf, limSup)

	m1 = str(s1)
	m1 += "\r\n"

	m2 = str(s2)
	m2 += "\r\n"

	ser.write(m1.encode())
	ser.write(m2.encode())


	print("s1 es", s1)
	print("s2 es", s2)

	time.sleep(0.5)
ser.close()
