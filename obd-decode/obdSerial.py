import time
import serial
import io
import socketio
import threading
import json
import datetime

num = 0
begin = False
stop = False
log = {}
fileName = ""
sio = socketio.Client()
sio.connect('http://localhost')

ser = serial.Serial(
	port='/dev/ttyUSB0',
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
                if res != "ELM327 v1.3a":
			raise Exception('Did not receive expected response')
		
		#STEP 2:
		#Attempt to send 'ATSP0'
		input = 'ATSP0'
		ser.write(input + '\r\n')
		time.sleep(1)
		ser.flush()
		res = []
		i = 0;
		while(ser.inWaiting() >1):
			res.append(ser.read()) #= ser.read()
			i += 1
		print(res)
                if res[6:8] != "OK":
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
                if res[0:2] != "41":
			raise Exception('Did not receive expected response')
			
	except Exception as error:
		print(repr(error))

def decode(res):
	data = [0,0]
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

def message_handler(msg):
	global begin, fileName, log, stop
	print('test: ', msg)
	begin = msg
	stop = False
	fileName = str(datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S"))
	with open(str(fileName+".json"), 'a') as outfile:
		outfile.write('[')

def stop_handler(msg):
	global stop
	print('test: ', msg)
	stop = msg
	
def send(res):
	global begin, stop
	data = decode(res)	
	sio.emit('obd-in', [data,data])
	print("Sent data to server")
	
	sio.on("start", message_handler)
	sio.on("stop", stop_handler)
	if(begin == True):
		log['date'] = datetime.datetime.now().isoformat()
		log['speed'] = data
		log['rpm'] = data
		with open(str(fileName+".json"), 'a') as outfile:
			json.dump((log), outfile)
			if(stop == True):
				outfile.write(']')
				begin = False
			else:
				outfile.write(',')
		print("finished logging")

def loop(num): 
	
	#init()
	while(1):
		input = '01 0C 0D'
		ser.write(input + '\r\n')
		time.sleep(0.1)
		ser.flush()
		res = ''
		while(ser.inWaiting() >1):
			res += ser.read()	
		t1 = threading.Thread(target=send, args=(res,))
		t1.start() 
		num = num + 1
	ser.close()
	
if __name__ == '__main__':
	loop(num)