import time
import serial
import io
import socketio
num = 0
sio = socketio.Client()
sio.connect('http://localhost')

ser = serial.Serial(
	port='COM3',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
)
def init():
	try:
		#STEP 1:
		#Attempt to send 'ATZ'
		input = 'ATZ'
		ser.write(input + '\r\n')
		time.sleep(1)
		ser.flush()
		res = ''
		while(ser.inWaiting() >1):
			res += ser.read()
		print("This is serial res")
		print(res)
		if res != "ELM327 v1.3a"
			raise Exception('Did not receive expected response')
		
		#STEP 2:
		#Attempt to send 'ATSP0'
		input = 'ATSP0'
		ser.write(input + '\r\n'*)
		time.sleep(1)
		ser.flush()
		res = []
		i = 0;
		while(ser.inWaiting() >1):
			res.append(ser.read()) #= ser.read()
			i += 1
		print(res)
		if res[6:8] != "OK"
			raise Exception('Did not receive expected response')
		
		#STEP 3:
		#Attempt to send '0100'
		input = '0100'
		ser.write(input + '\r\n')
		#we need to test reducing this
		time.sleep(5)
		ser.flush()
		res = ''
		while(ser.inWaiting() >1):
			res += ser.read()
		print(res)
		if res[0:2] != "41"
			raise Exception('Did not receive expected response')
			
	except Exception as error:
		print(repr(error))

def decode(res):
	data[0,0]
	hexnumber = res.split("\r")
	hexnumber = hexnumber[1].split(" ")
	for x in range(len(hexnumber)):
		if (x == 1):
			A = int(hexnumber[x+1],16)
			B = int(hexnumber[x+2],16)
			rpm = (256*A + B)/4
			data[0] = rpm
			print('RPM : '+ repr(rpm))
		if (x==4):
			A = int(hexnumber[x+1],16)
			MPH = int(A*(.621))
			data[1] = MPH
			print('MPH : '+ repr(MPH))
	return data

def loop(num):
	init()
	while(1):
		input = '01 0C 0D'
		ser.write(input + '\r\n')
		time.sleep(0.1)
		ser.flush()
		res = ''
		while(ser.inWaiting() >1):
			res += ser.read()
		data = decode(res)
		sio.emit('obd-in', data)
	ser.close()
	
if __name__ == '__main__':
	loop(num)
	
	
	"""
	while(1):
		if num == 141:
			num = 0
		sio.emit('obd-in', [num,num])
		num = num + 1
		time.sleep(0.1)
	"""
	