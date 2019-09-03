import time
import serial
import io
import socketio
import threading
import json
import datetime

begin = False
stop = False
OBDtime = ""
log = {}
fileName = ""
response = []

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


def logging(data):
    global begin, fileName, log, stop
    sockets.on("start", message_handler)
    sockets.on("stop", stop_handler)
    if (begin == True):
        log['date'] = datetime.datetime.now().isoformat()
        log['speed'] = data[1]
        log['rpm'] = data[0]
        # log gps coords here
        with open(str(fileName + ".json"), 'a') as outfile:
            json.dump((log), outfile)
            if (stop == True):
                outfile.write(']')
                # stop recording video
                begin = False
            else:
                outfile.write(',')
        print("finished logging")


def decode(res):
	OBD_DICT = {'00': 0, '05': 1, '0C': 2, '0D': 1, '0F': 1, '11': 1}

	for i in range(1, len(my_list)):
		if '0:' in my_list[i]:
			a = my_list[i]
			a = a.replace('0: ', '')
		if '1:' in my_list[i]:
			b = my_list[i]
			b = b.replace('1: ', '')
	new_string = a + b
	new_string = new_string.replace('\n', '')
	obd_string = new_string.split(' ')
	obd_string.remove(obd_string[-1])

	i = 2
	while i < len(obd_string):
		obd_code = OBD_DICT[obd_string[i]]
		if obd_code == 2:
			A = int(obd_string[i + 1], 16)
			B = int(obd_string[i + 2], 16)
			obd_data = (256 * A + B) / 4
			print('RPM : ' + repr(obd_data))
		elif obd_code == 1:
			A = int(obd_string[i + 1], 16)
			if (obd_string[i] == "05"):
				obd_data = A - 40
				print('Engine coolant temperature :' + repr(obd_data))
			elif (obd_string[i] == "0D"):
				obd_data = int(A * (.621))
				print('MPH : ' + repr(obd_data))
			elif (obd_string[i] == "0F"):
				obd_data = A - 40
				print('Intake Air Temperature :' + repr(obd_data))
			elif (obd_string[i] == "11"):
				obd_data = float((float(100) / 255) * A)
				print('Throttle Position :' + repr(obd_data))
		i += (obd_code + 1)
	return data


def message_handler(msg):
	global begin, fileName, log, stop
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
		OBDtime = datetime.datetime.now().isoformat()


def loop():
	global response, begin, stop, OBDtime
	init()
	t1 = threading.Thread(target=read)
	t1.start()
	while (1):
		gps = "GPS DATA"        #go get GPS data
		time.sleep(0.1)
		if (response != []):
			data = decode(res)	  #fix decoder
			sockets.emit('obd-in', data)
			print(response)
			response = []
			obdTime = ""
		logging(data,gps,obdTime)
		print(datetime.datetime.now().isoformat())


if __name__ == '__main__':
	try:
		loop()
	except KeyboardInterrupt:
		sio.close()