import time
import serial
import io

ser = serial.Serial(
	port='COM3',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
)

input = 'ATZ'
ser.write(input + '\r\n')
ser.flush()
time.sleep(1)
res = ''
while(ser.inWaiting() >1):
	res += ser.read()
print(res)
print("This is serial res")
print(res)


input = 'ATSP0'
ser.write(input + '\r\n')
time.sleep(1)
ser.flush()
res = []
i = 0;
while(ser.inWaiting() >0):
	res.append(ser.read()) #= ser.read()
	i += 1
print(res)

input = '0100'
ser.write(input + '\r\n')
time.sleep(5)
ser.flush()
res = ''
while(ser.inWaiting() >1):
	res += ser.read()
print(res)

while(1):
	input = '01 0C 0D'
	ser.write(input + '\r\n')
	time.sleep(0.1)
	ser.flush()
	res = ''
	while(ser.inWaiting() >1):
		res += ser.read()
	#print(res)
	hexnumber = res.split("\r")
	hexnumber = hexnumber[1].split(" ")
	for x in range(len(hexnumber)):
		if (x == 1):
			A = int(hexnumber[x+1],16)
			B = int(hexnumber[x+2],16)
			rpm = (256*A + B)/4
			print('RPM : '+ repr(rpm))
		if (x==4):
			A = int(hexnumber[x+1],16)
			MPH = int(A*(.621))
			print('MPH : '+ repr(MPH))

ser.close()