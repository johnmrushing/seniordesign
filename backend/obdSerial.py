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
	if (res[i] == '>'):
		print("Hello")
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
	input = '01 05 0C'
	ser.write(input + '\r\n')
	time.sleep(0.1)
	ser.flush()
	res = ''
	while(ser.inWaiting() >1):
		res += ser.read()
	print(res)




ser.close()