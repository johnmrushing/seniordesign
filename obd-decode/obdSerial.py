import time
import serial
import io
#import socketio
import threading
import json
import datetime

begin = False
stop = False
OBDtime = ""
log = {}
fileName = ""
response = []

ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=10000,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=0.1,#0.01
)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

def init():
	try:
		#STEP 1:
		#Attempt to send 'ATZ'
		input = 'ATZ\r'
		sio.write(unicode(input))
		sio.flush()
		time.sleep(1)
		res = sio.readlines()
		print("This is serial res")
		print(res)
		
		#STEP 2:
		#Attempt to send 'ATSP0'
		input = 'ATSP0\r'
		sio.write(unicode(input))
		sio.flush()
		time.sleep(1)
		res = sio.readlines()
		print(res)
		
		#STEP 3:
		#Attempt to send '0100'
		input = '0100\r'
		sio.write(unicode(input))
		#we need to test reducing this
		sio.flush()
		time.sleep(10)
		res = sio.readlines()
		print(res)
		
		input = 'at h1\r'
		sio.write(unicode(input))
		sio.flush()
		time.sleep(1)
		res = sio.readlines()
		print(res)
		
		
	except Exception as error:
		print(repr(error))

def logging(data):
	global begin, fileName, log, stop
	sio.on("start", begin_handler)
	sio.on("stop", stop_handler)
	if(begin == True):
		log['date'] = datetime.datetime.now().isoformat()
		log['speed'] = data[1]
		log['rpm'] = data[0]
		#log gps coords here
		with open(str(fileName+".json"), 'a') as outfile:
			json.dump((log), outfile)
			if(stop == True):
				outfile.write(']')
				#stop recording video
				begin = False
			else:
				outfile.write(',')
		print("finished logging")
		
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

def read():
	global response, OBDtime
	input = '01 0C 0D 0F 05 11\r'
	sio.write(unicode(input))
	sio.flush()
	#time.sleep(0.1)
	response = sio.readlines()
	OBDtime = datetime.datetime.now().isoformat()
	
	
def loop(): 
	global response, begin, stop,OBDtime
	init()
	while(1):
		response = []
		t1 = threading.Thread(target=read)
		t1.start() 
		#gps =go get GPS data
		
		if(response != []):
			data = decode(res)	  #fix decoder
			sio.emit('obd-in', data)	
			print(OBDtime)
			print(response)
		logging(data,gps,obdTime)
	
	
if __name__ == '__main__':
	loop()