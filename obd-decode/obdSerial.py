import time
import serial
import io
import socketio
import threading
import json
import datetime

begin = False
stop = False
newOBD = False
OBDtime = ""
log = {}
fileName = ""
response = []

OBD_DICT = {'00': 0, '05': 1, '0C': 2, '0D': 1, '0F': 1, '11': 1}
OBD_LOG = {'Engine coolant temperature': 0, 'Engine RPM': 0, 'Vehicle Speed': 0, 'Intake Air Temperature': 0,'Throttle Position': 0}
OBD_FUNC = {'05': ECT_Decode, '0C': RPM_Decode, '0D': MPH_Decode, '0F': IAT_Decode, '11': TP_Decode}

sockets = socketio.Client()
sockets.connect('http://localhost')
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=10000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.01,
)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

def init():
    try:
        # STEP 1:
        # Attempt to send 'ATZ'
        input = 'ATZ\r'
        sio.write(unicode(input))
        sio.flush()
        time.sleep(1)
        res = sio.readlines()
        print("This is serial res")
        print(res)

        # STEP 2:
        # Attempt to send 'ATSP0'
        input = 'ATSP0\r'
        sio.write(unicode(input))
        sio.flush()
        time.sleep(1)
        res = sio.readlines()
        print(res)

        # STEP 3:
        # Attempt to send '0100'
        input = '0100\r'
        sio.write(unicode(input))
        # we need to test reducing this
        sio.flush()
        time.sleep(10)
        res = sio.readlines()
        print(res)

        # input = 'ATAT0\r'
        # sio.write(unicode(input))
        # sio.flush()
        # time.sleep(1)
        # res = sio.readlines()
        # print(res)
		#
        # input = 'at st 16\r'
        # sio.write(unicode(input))
        # sio.flush()
        # time.sleep(1)
        # res = sio.readlines()
        # print(res)
    except Exception as error:
        print(repr(error))

def ECT_Decode():
	A = int(obd_string[i + 1], 16)
	OBD_data = A - 40
	OBD_LOG['Engine coolant temperature'] = OBD_data

def RPM_Decode():
	A = int(obd_string[i + 1], 16)
	B = int(obd_string[i + 2], 16)
	OBD_data = (256 * A + B) / 4
	OBD_LOG['Engine RPM'] = OBD_data
def MPH_Decode():
	A = int(obd_string[i + 1], 16)
	OBD_data = int(A * (.621))
	OBD_LOG['Vehicle Speed'] = OBD_data
def IAT_Decode():
	A = int(obd_string[i + 1], 16)
	OBD_data = A - 40
	OBD_LOG['Intake Air Temperature'] = OBD_data
def TP_Decode():
	A = int(obd_string[i + 1], 16)
	OBD_data = round(float((float(100) / 255) * A), 3)
	OBD_LOG['Throttle Position'] = OBD_data

def decode(rawData):
	global OBD_DICT, OBD_LOG, OBD_FUNC
	OBD_LOG = {'Engine coolant temperature': 0, 'Engine RPM': 0, 'Vehicle Speed': 0, 'Intake Air Temperature': 0,'Throttle Position': 0}
	a = ''
	b = ''
	for i in range(1, len(rawData)):
		if '0:' in rawData[i]:
			a = rawData[i]
			if (len(a) < 20):
				a = a + rawData[i + 1]
			a = a.replace('0: ', '')
		if '1:' in rawData[i]:
			b = rawData[i]
			if (len(b) < 20):
				b = b + rawData[i + 1]
			b = b.replace('1: ', '')
		if (len(a) > 2 and len(b) > 2):
			break

	new_string = a + b
	new_string = new_string.replace('\n', '')
	obd_string = new_string.split(' ')
	obd_string.remove(obd_string[-1])

	i = 1
	while i < len(obd_string):
		obd_code = OBD_DICT[obd_string[i]]
		if (obd_code != 0):
			OBD_FUNC[obd_string[i]]()
		# print(obd_data)
		i += (obd_code + 1)

def logging(gps, obdTime):
    global begin, fileName, log, stop
    sockets.on("start", message_handler)
    sockets.on("stop", stop_handler)
    if (begin == True):
        OBD_LOG['GPS'] = gps
        OBD_LOG['OBD Time'] = obdTime
        with open(str(fileName + ".json"), 'a') as outfile:
            json.dump(OBD_LOG, outfile)
            if (stop == True):
                outfile.write(']')
                # stop recording video
                begin = False
            else:
                outfile.write(',')
        print("finished logging")

def message_handler(msg):
	global begin, fileName, stop
	print('test: ', msg)
	begin = msg
	stop = False
	fileName = str(datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S"))
	with open(str(fileName + ".json"), 'a') as outfile:
		outfile.write('[')

def stop_handler(msg):
	global stop
	print('test: ', msg)
	stop = msg

def read():
	global response, OBDtime
	while (1):
		input = '01 0C 0D 0F 05 11\r'
		sio.write(unicode(input))
		sio.flush()
		time.sleep(0.1)
		response = sio.readlines()
		newOBD = True
		OBDtime = datetime.datetime.now().isoformat()

def loop():
	global response, begin, stop, OBDtime, newOBD
	data = ""
	init()
	t1 = threading.Thread(target=read)
	t1.start()
	while (1):
		gps = "GPS DATA" #go get GPS data
		time.sleep(0.1)
		if (newOBD == True):
			decode(response)
			data = json.dump(OBD_LOG)
			sockets.emit('obd-in', data)
			print(data)
			newOBD = False
		logging(gps, obdTime)
		print(datetime.datetime.now().isoformat())

if __name__ == '__main__':
	try:
		loop()
	except KeyboardInterrupt:
		sio.close()