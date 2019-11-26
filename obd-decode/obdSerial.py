import time
import serial
import io
import socketio
import threading
import json
import datetime
import os
import picamera
import subprocess
from gps.gps import GPS

camera = ""
audio_proc= ""
outfilenamevideo= ""
outfilenameaudio= ""
outfilenamemp3= ""
encoded_filename= ""
encoded_filename2= ""
videoSetting = True;
begin = False
stop = False
newOBD = False
initialBegin = False
newGPS = False
obd_string = ""
i= 0
OBDtime = ""
log = {}
fileName = ""
response = []
VIN = ""
t2= ""
possibleCodes= []
selectedCodes = ["","","","Engine RPM","",""]
selectedCodesString = "01 0C"
GPSData = ""
myGPS= GPS()

sockets = socketio.Client()
sockets.connect('http://localhost')
ser = serial.Serial(
    port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A90855PO-if00-port0',
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
		sio.write(str(input))
		sio.flush()
		time.sleep(1)
		res = sio.readlines()
		print("This is serial res")
		print(res)

		# STEP 2:
		# Attempt to send 'ATSP0'
		input = 'ATSP0\r'
		sio.write(str(input))
		sio.flush()
		time.sleep(1)
		res = sio.readlines()
		print(res)

		# STEP 3:
		# Attempt to send '0100'
		input = '0100\r'
		sio.write(str(input))
		# we need to test reducing this
		sio.flush()
		time.sleep(10)
		res = sio.readlines()
		print(res)

		# STEP 4:
		# Attempt to send '0902' for VIN
		input = '0902\r'
		sio.write(str(input))
		sio.flush()
		time.sleep(2)
		res = sio.readlines()
		print(res)
		VIN_Decode(res)
	except Exception as error:
		print(repr(error))

def VIN_Decode(res):
	global VIN, possibleCodes
	print(res)
	#decodedVin = ... res to get vin
	for i in range(1,len(res)):
		if '0:' in res[i]:
			a = res[i]
			a = a.replace('0: ','')
		if '1:' in res[i]:
			b = res[i]
			b = b.replace('1: ','')
		if '2:' in res[i]:
			c = res[i]
			c = c.replace('2: ','')
	VIN_hex = a+b+c
	VIN_hex = VIN_hex[3:]    
	VIN_hex = VIN_hex.replace(' ','')
	VIN_hex = VIN_hex.replace('\n','')
	VIN = bytes.fromhex(VIN_hex).decode('utf-8')
	print(VIN)
	contents = ""
	if(os.path.exists('profiles/'+VIN+'.txt')):
		f = open('profiles/'+VIN+'.txt')
		contents = json.loads(f.read())
		possibleCodes = contents
		sockets.emit('possibleCodes', possibleCodes)
		f.close()
		#need to figure out where we want to convert codes to string
	else:
		possibleCodes = possibleCodesScan()
		print(possibleCodes)
		f = open('profiles/'+VIN+'.txt',"w+")
		f.write(json.dumps(possibleCodes))
		sockets.emit('possibleCodes', possibleCodes)
		f.close()
		
def possibleCodesScan():
	work = []
	dontwork = []
	for i in OBD_CODES:
		input = "01" + OBD_CODES[i] + "\r"
		sio.write(str(input))
		sio.flush()
		time.sleep(0.2)
		response = sio.readlines()
		print(response)
		for j in range(0,len(response)):
			if j == 1:
				if(response[j] != u'NO DATA\n'):
					work.append(i)
				else:
					dontwork.append(i)

	print("Scan is complete")
	return work

def CEL_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = round(float(100/255)*A,3)
    OBD_LOG['Calculated Engine Load'] = OBD_data

def ECT_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = A - 40
    OBD_LOG['Engine Coolant Temperature'] = OBD_data

def STFTB1_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round((float(100/255)*A) - 100,3)
	OBD_LOG['Short Term Fuel Trim-Bank 1'] = OBD_data
	
def LTFTB1_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round((float(100/255)*A) - 100,3)
	OBD_LOG['Long Term Fuel Trim-Bank 1'] = OBD_data
	
def STFTB2_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = (round(float(100/255)*A) - 100,3)
	OBD_LOG['Short Term Fuel Trim-Bank 2'] = OBD_data
	
def LTFTB2_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round((float(100/255)*A) - 100,3)
	OBD_LOG['Long Term Fuel Trim-Bank 2'] = OBD_data
	
def FPGP_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = 3*A
	OBD_LOG['Fuel Pressure'] = OBD_data
	
def RPM_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = round((256*A+B)/4)
    OBD_LOG['Engine RPM'] = OBD_data
    
def MPH_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = int(A*(.621))
	OBD_LOG['Vehicle Speed'] = OBD_data
	print(OBD_data)
    
def TA_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = (A/2)-64
	OBD_LOG['Timing Advance'] = OBD_data
	
def IAT_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = A - 40
    OBD_LOG['Intake Air Temperature'] = OBD_data

def MAFAFR_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A+B)/100
    OBD_LOG['MAF Air Flow Rate'] = OBD_data
	
def TP_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = round(float((float(100)/255)*A),3)
    OBD_LOG['Throttle Position'] = OBD_data

def OSVSTFTB1_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = A/200
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Oxygen Sensor 1: Voltage'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 1: Short Term Fuel Trim'] = OBD_data_2
	
def OSVSTFTB2_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = A/200
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Oxygen Sensor 2: Voltage'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 2: Short Term Fuel Trim'] = OBD_data_2

def OSVSTFTB3_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = A/200
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Oxygen Sensor 3: Voltage'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 3: Short Term Fuel Trim'] = OBD_data_2
	
def OSVSTFTB4_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = A/200
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Oxygen Sensor 4: Voltage'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 4: Short Term Fuel Trim'] = OBD_data_2

def OSVSTFTB5_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = A/200
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Oxygen Sensor 5: Voltage'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 5: Short Term Fuel Trim'] = OBD_data_2
	
def OSVSTFTB6_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = A/200
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Oxygen Sensor 6: Voltage'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 6: Short Term Fuel Trim'] = OBD_data_2
	
def OSVSTFTB7_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = A/200
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Oxygen Sensor 7: Voltage'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 7: Short Term Fuel Trim'] = OBD_data_2

def OSVSTFTB8_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = A/200
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Oxygen Sensor 8: Voltage'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 8: Short Term Fuel Trim'] = OBD_data_2

def RTSES_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A)+B
    OBD_LOG['Run Time Since Engine Start'] = OBD_data
	
def DTWMILO_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A)+B
    OBD_LOG['Distance Traveled With Malfunction Indicator Lamp (MIL) On'] = OBD_data
	
def FRP_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = round(0.079*(256*A+B),3)
    OBD_LOG['Fuel Rail Pressure'] = OBD_data
	
def FRGP_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = 10*(256*A+B)
    OBD_LOG['Fuel Rail Gauge Pressure'] = OBD_data
	
def OSABCDFAERVB1_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = round(float(8/65536)*(256*C+D),3)
	OBD_LOG['Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 1 CD: Voltage'] = OBD_data_2

def OSABCDFAERVB5_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = round(float(8/65536)*(256*C+D),3)
	OBD_LOG['Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 1 CD: Voltage'] = OBD_data_2
	
def OSABCDFAERVB6_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = round(float(8/65536)*(256*C+D),3)
	OBD_LOG['Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 1 CD: Voltage'] = OBD_data_2
	
def OSABCDFAERVB8_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = round(float(8/65536)*(256*C+D),3)
	OBD_LOG['Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 1 CD: Voltage'] = OBD_data_2
	
def CEGR_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = round(float(100/255)*A,3)
    OBD_LOG['Commanded EGR'] = OBD_data

def EGRE_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = round(float(100/255)*A - 100,3)
    OBD_LOG['EGR Error'] = OBD_data
	
def CEP_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = round(float(100/255)*A,3)
    OBD_LOG['Commanded Evaporative Purge'] = OBD_data

def FTLI_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round(float(100/255)*A,3)
	OBD_LOG['Fuel Tank Level Input'] = OBD_data

def WUSCC_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = A
    OBD_LOG['Warm-ups Since Codes Cleared'] = OBD_data

def DTSCC_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A+B)
    OBD_LOG['Distance Traveled Since Codes Cleared'] = OBD_data
	
def ESVP2C_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A+B)/4
    OBD_LOG['Evap. System Vapor Pressure 2 complements'] = OBD_data
	
def ABP_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = A
	OBD_LOG['Absolute Barometric Pressure'] = OBD_data
	
def OSABCDFAERCB1_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 1 CD: Voltage'] = OBD_data_2

def OSABCDFAERCB2_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 2 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 2 CD: Voltage'] = OBD_data_2

def OSABCDFAERCB3_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 3 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 3 CD: Voltage'] = OBD_data_2
	
def OSABCDFAERCB4_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 4 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 4 CD: Voltage'] = OBD_data_2
	
def OSABCDFAERCB5_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 5 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 5 CD: Voltage'] = OBD_data_2

def OSABCDFAERCB6_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 6 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 6 CD: Voltage'] = OBD_data_2
	
def OSABCDFAERCB7_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 7 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 7 CD: Voltage'] = OBD_data_2

def OSABCDFAERCB8_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = round(float(2/65536)*(256*A+B),3)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 8 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 8 CD: Voltage'] = OBD_data_2
	
def CTB1S1_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A+B)/10 - 40
    OBD_LOG['Catalyst Temperature: Bank 1, Sensor 1'] = OBD_data
	
def CTB2S1_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A+B)/10 - 40
    OBD_LOG['Catalyst Temperature: Bank 2, Sensor 1'] = OBD_data
	
def CTB1S2_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A+B)/10 - 40
    OBD_LOG['Catalyst Temperature: Bank 1, Sensor 2'] = OBD_data
	
def CTB2S2_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A+B)/10 - 40
    OBD_LOG['Catalyst Temperature: Bank 2, Sensor 2'] = OBD_data
	
def CMV_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = (256*A+B)/1000
	OBD_LOG['Control Module Voltage'] = OBD_data
	
def ALV_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = round(float(100/255)*(256*A+B),3)
	OBD_LOG['Absolute Load Value'] = OBD_data
	
def FACER_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = round(float(2/65536)*(256*A+B),3)
	OBD_LOG['Fuel-Air Commanded Equivalence Ratio'] = OBD_data
	
def RTP_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round(float(100/255)*A,3)
	OBD_LOG['Relative Throttle Position'] = OBD_data
	
def AAT_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = A - 40
	OBD_LOG['Ambient Air Temperature'] = OBD_data
	
def ATPB_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round(float(100/255)*A,3)
	OBD_LOG['Absolute Throttle Position B'] = OBD_data

def ATPC_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round(float(100/255)*A,3)
	OBD_LOG['Absolute Throttle Position C'] = OBD_data	

def APPD_Decode(): 
	A = int(obd_string[i+1],16)
	OBD_data = round(float(100/255)*A,3)
	OBD_LOG['Absolute Throttle Position D'] = OBD_data
	
def APPE_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round(float(100/255)*A,3)
	OBD_LOG['Absolute Throttle Position E'] = OBD_data

def APPF_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round(float(100/255)*A,3)
	OBD_LOG['Absolute Throttle Position F'] = OBD_data
	
def CTA_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round(float(100/255)*A,3)
	OBD_LOG['Commanded Throttle Actuator'] = OBD_data
	
def TRWMILO_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = (256*A+B)
	OBD_LOG['Time Run With MIL On'] = OBD_data
	
def TSTCC_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = round(float(2/65536)*(256*A+B),3)
	OBD_LOG['Time Since Trouble Codes Cleared'] = OBD_data

def MVFFAEROSVOSCAIMAP_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data = 10*D
	OBD_LOG['Maximum Value For Fuel-Air Equivalence Ratio'] = A
	OBD_LOG['Maximum Value For Oxygen Sensor Voltage'] = B
	OBD_LOG['Maximum Value For Oxygen Sensor Current'] = C
	OBD_LOG['Maximum Value For Intake Manifold Absolute Pressure'] = OBD_data

def MVFAFRFMAFS_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data = 10*A
	OBD_LOG['Maximum Value For Air Flow From Mass Air Flow Sensor'] = A

def EF_Decode(): 
	A = int(obd_string[i+1],16)
	OBD_data = round(float(100/255)*A,3)
	OBD_LOG['Ethanol Fuel Percent'] = OBD_data
	
def AESVP_Decode(): 
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = ((256*A+B)/200)
	OBD_LOG['Absolute Evap System Vapor Pressure'] = OBD_data
	
def ESVP_Decode(): 
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = ((A*256)+B)-32767
	OBD_LOG['Evap System Vapor Pressure'] = OBD_data

def STSOSTAB1BB3_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = round((float(100/128)*A)-100,3)
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Short Term Secondary Oxygen Sensor Trim, A: Bank 1'] = OBD_data_1
	OBD_LOG['Short Term Secondary Oxygen Sensor Trim, B: Bank 3'] = OBD_data_2
	
def LTSOSTAB1BB3_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = round((float(100/128)*A)-100,3)
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Long Term Secondary Oxygen Sensor Trim, A: Bank 1'] = OBD_data_1
	OBD_LOG['Long Term Secondary Oxygen Sensor Trim, B: bank 3'] = OBD_data_2
	
def STSOSTAB2BB4_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = round((float(100/128)*A)-100,3)
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Short Term Secondary Oxygen Sensor Trim, A: bank 2'] = OBD_data_1
	OBD_LOG['Short Term Secondary Oxygen Sensor Trim, B: bank 4'] = OBD_data_2
	
def LTSOSTAB2BB4_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = round((float(100/128)*A)-100,3)
	OBD_data_2 = round((float(100/128)*B)-100,3)
	OBD_LOG['Long Term Secondary Oxygen Sensor Trim, A: bank 2'] = OBD_data_1
	OBD_LOG['Long Term Secondary Oxygen Sensor Trim, B: bank 4'] = OBD_data_2
	
def FRAP_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = 10*(256*A+B)
	OBD_LOG['Fuel Rail Absolute Pressure'] = OBD_data

def RAPP_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round((100/255)*A,3)
	OBD_LOG['Relative Accelerator Pedal Position'] = OBD_data
	
def HBPRL_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = round((100/255)*A,3)
	OBD_LOG['Hybrid Battery Pack Remaining Life'] = OBD_data
	
def EOT_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = A - 40
	OBD_LOG['Engine Oil Temperature'] = OBD_data

def FIT_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = ((256*A+B)/128)-210
	OBD_LOG['Fuel Injection Timing'] = OBD_data
	
def EFR_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = ((256*A+B)/20)
	OBD_LOG['Engine Fuel Rate'] = OBD_data

def DDEPT_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = A-125
	OBD_LOG['Drivers Demand Engine-Percent Torque'] = OBD_data
	
def AEPT_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = A-125
	OBD_LOG['Actual Engine-Percent Torque'] = OBD_data

def ERT_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = (256*A+B)
	OBD_LOG['Engine Reference Torque'] = OBD_data
	
OBD_DICT = {'00' : 0,'04' : 1,'05' : 1,'06' : 1,'07' : 1,'08' : 1,'09' : 1,'0A' : 1,'0C' : 2,'0D' : 1,'0E' : 1,'0F' : 1,'10' : 2,'11' : 1,'14' : 2,'15' : 2,'16' : 2,'17' : 2,'18' : 2,'19' : 2,'1A' : 2,'1B' : 2,'1F' : 2,'21' : 2,'22' : 2,'23' : 2,'24' : 4,'28' : 4,'29' : 4,'2B' : 4,'2C' : 1,'2D' : 1,'2E' : 1,'30' : 1,'31' : 2,'32' : 2,'33' : 1,'34' : 4,'35' : 4,'36' : 4,'37' : 4,'38' : 4,'39' : 4,'3A' : 4,'3B' : 4,'3C' : 2,'3D' : 2,'3E' : 2,'3F' : 2,'42' : 2,'43' : 2,'44' : 2,'45' : 1,'46' : 1,'47' : 1,'48' : 1,'49' : 1,'4A' : 1,'4B' : 1,'4C' : 1,'4D' : 2,'4E' : 2,'4F' : 4,'50' : 4,'52' : 1,'53' : 2,'54' : 2,'55' : 2,'56' : 2,'57' : 2,'58' : 2,'59' : 2,'5A': 1,'5B' : 1,'5C' : 1,'5D' : 2,'5E' : 2,'61' : 1,'62' : 1,'63' : 2}
OBD_LOG = {}
OBD_FUNC = {'04' : CEL_Decode,'05' : ECT_Decode,'06' : STFTB1_Decode,'07' : LTFTB1_Decode,'08' : STFTB2_Decode,'09' : LTFTB2_Decode,'0A' : FPGP_Decode,'0C' : RPM_Decode,'0D' : MPH_Decode,'0E' : TA_Decode,'0F' : IAT_Decode,'10' : MAFAFR_Decode,'11' : TP_Decode,'14' : OSVSTFTB1_Decode,'15' : OSVSTFTB2_Decode,'16' : OSVSTFTB3_Decode,'17' : OSVSTFTB4_Decode,'18' : OSVSTFTB5_Decode,'19' : OSVSTFTB6_Decode,'1A' : OSVSTFTB7_Decode,'1B' : OSVSTFTB8_Decode,'1F' : RTSES_Decode,'21' : DTWMILO_Decode,'22' : FRP_Decode,'23' : FRGP_Decode,'24' : OSABCDFAERVB8_Decode,'28' : OSABCDFAERVB5_Decode,'29' : OSABCDFAERVB6_Decode,'2B' : OSABCDFAERVB8_Decode,'2C' : CEGR_Decode,'2D' : EGRE_Decode,'2E' : CEP_Decode,'2F' : FTLI_Decode,'30' : WUSCC_Decode,'31' : DTSCC_Decode,'32' : ESVP2C_Decode,'33' : ABP_Decode,'34' : OSABCDFAERCB1_Decode,'35' : OSABCDFAERCB2_Decode,'36' : OSABCDFAERCB3_Decode,'37' : OSABCDFAERCB4_Decode,'38' : OSABCDFAERCB5_Decode,'39' : OSABCDFAERCB6_Decode,'3A' : OSABCDFAERCB7_Decode,'3B' : OSABCDFAERCB8_Decode,'3C' : CTB1S1_Decode,'3D' : CTB2S1_Decode,'3E' : CTB1S2_Decode,'3F' : CTB2S2_Decode,'42' : CMV_Decode,'43' : ALV_Decode,'44' : FACER_Decode,'45' : RTP_Decode,'46' : AAT_Decode,'47' : ATPB_Decode,'48' : ATPC_Decode,'49' : APPD_Decode,'4A' : APPE_Decode,'4B' : APPF_Decode,'4C' : CTA_Decode,'4D' : TRWMILO_Decode,'4E' : TSTCC_Decode,'4F' : MVFFAEROSVOSCAIMAP_Decode,'50' : MVFAFRFMAFS_Decode,'52' : EF_Decode,'53' : AESVP_Decode,'54' : ESVP_Decode,'55' : STSOSTAB1BB3_Decode,'56' : LTSOSTAB1BB3_Decode,'57' : STSOSTAB2BB4_Decode,'58' : LTSOSTAB2BB4_Decode,'59' : FRAP_Decode,'5A' : RAPP_Decode,'5B' : HBPRL_Decode,'5C' : EOT_Decode,'5D' : FIT_Decode,'5E' : EFR_Decode,'61' : DDEPT_Decode,'62' : AEPT_Decode,'63' : ERT_Decode,'67' : ECT_Decode}

OBD_CODES ={
  'Vehicle Speed': '0D',
  'Engine RPM': '0C',
  'Intake Air Temperature': '0F',
  'Engine Coolant Temperature': '67',
  'Throttle Position': '11',
  'Evap System Vapor Pressure': '54',
  'Maximum Value For Air Flow From Mass Air Flow Sensor': '50',
  'Calculated Engine Load': '04',
  'Evap. System Vapor Pressure': '32',
  'Ambient Air Temperature': '46',
  'Oxygen Sensor 1: Voltage': '14',
  'Oxygen Sensor 1: Short Term Fuel Trim': '14',
  'Oxygen Sensor 2: Voltage': '15',
  'Oxygen Sensor 2: Short Term Fuel Trim': '15',
  'Oxygen Sensor 3: Voltage': '16',
  'Oxygen Sensor 3: Short Term Fuel Trim': '16',
  'Oxygen Sensor 4: Voltage': '17',
  'Oxygen Sensor 4: Short Term Fuel Trim': '17',
  'Oxygen Sensor 5: Voltage': '18',
  'Oxygen Sensor 5: Short Term Fuel Trim': '18',
  'Oxygen Sensor 6: Voltage': '19',
  'Oxygen Sensor 6: Short Term Fuel Trim': '19',
  'Oxygen Sensor 7: Voltage': '1A',
  'Oxygen Sensor 7: Short Term Fuel Trim': '1A',
  'Oxygen Sensor 8: Voltage': '1B',
  'Oxygen Sensor 8: Short Term Fuel Trim': '1B',
  'Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio': '24',
  'Oxygen Sensor 1 CD: Voltage': '24',
  'Oxygen Sensor 2 AB: Fuel-Air Equivalence Ratio': '25',
  'Oxygen Sensor 2 CD: Voltage': '25',
  'Oxygen Sensor 3 AB: Fuel-Air Equivalence Ratio': '26',
  'Oxygen Sensor 3 CD: Voltage': '26',
  'Oxygen Sensor 4 AB: Fuel-Air Equivalence Ratio': '27',
  'Oxygen Sensor 4 CD: Voltage': '27',
  'Oxygen Sensor 5 AB: Fuel-Air Equivalence Ratio': '28',
  'Oxygen Sensor 5 CD: Voltage': '28',
  'Oxygen Sensor 6 AB: Fuel-Air Equivalence Ratio': '29',
  'Oxygen Sensor 6 CD: Voltage': '29',
  'Oxygen Sensor 7 AB: Fuel-Air Equivalence Ratio': '2A',
  'Oxygen Sensor 7 CD: Voltage': '2A',
  'Oxygen Sensor 8 AB: Fuel-Air Equivalence Ratio': '2B',
  'Oxygen Sensor 8 CD: Voltage': '2B',
  'Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio 2': '34',
  'Oxygen Sensor 1 CD: Current': '34',
  'Oxygen Sensor 2 AB: Fuel-Air Equivalence Ratio 2': '35',
  'Oxygen Sensor 2 CD: Current': '35',
  'Oxygen Sensor 3 AB: Fuel-Air Equivalence Ratio 2': '36',
  'Oxygen Sensor 3 CD: Current': '36',
  'Oxygen Sensor 4 AB: Fuel-Air Equivalence Ratio 2': '37',
  'Oxygen Sensor 4 CD: Current': '37',
  'Oxygen Sensor 5 AB: Fuel-Air Equivalence Ratio 2': '38',
  'Oxygen Sensor 5 CD: Current': '38',
  'Oxygen Sensor 6 AB: Fuel-Air Equivalence Ratio 2': '39',
  'Oxygen Sensor 6 CD: Current': '39',
  'Oxygen Sensor 7 AB: Fuel-Air Equivalence Ratio 2': '3A',
  'Oxygen Sensor 7 CD: Current': '3A',
  'Oxygen Sensor 8 AB: Fuel-Air Equivalence Ratio 2': '3B',
  'Oxygen Sensor 8 CD: Current': '3B',
  'Maximum Value For Fuel-Air Equivalence Ratio': '4F',
  'Maximum Value For Oxygen Sensor Voltage': '4F',
  'Maximum Value For Oxygen Sensor Current': '4F',
  'Maximum Value For Intake Manifold Absolute Pressure': '4F',
  'Short Term Secondary Oxygen Sensor Trim, A: Bank 1': '55',
  'Short Term Secondary Oxygen Sensor Trim, B: Bank 3': '55',
  'Long Term Secondary Oxygen Sensor Trim, A: Bank 1': '56',
  'Long Term Secondary Oxygen Sensor Trim, B: bank 3': '56',
  'Short Term Secondary Oxygen Sensor Trim, A: bank 2': '57',
  'Short Term Secondary Oxygen Sensor Trim, B: bank 4': '57',
  'Long Term Secondary Oxygen Sensor Trim, A: bank 2': '58',
  'Long Term Secondary Oxygen Sensor Trim, B: bank 4': '58',
  'Fuel-Air Commanded Equivalence Ratio': '44',
  'Hybrid Battery Pack Remaining Life': '5B',
  'Actual Engine-Percent Torque': '62',
  'Relative Accelerator Pedal Position': '5A',
  'Distance Traveled Since Codes Cleared': '31',
  'Drivers Demand Engine-Percent Torque': '61',
  'Engine Fuel Rate': '5E',
  'Absolute Evap System Vapor Pressure': '53',
  'Run Time Since Engine Start': '1F',
  'Fuel Injection Timing': '5D',
  'Long Term Fuel Trim-Bank 1': '07',
  'Long Term Fuel Trim-Bank 2': '09',
  'Catalyst Temperature: Bank 1, Sensor 2': '3E',
  'Catalyst Temperature: Bank 1, Sensor 1': '3C',
  'Commanded Throttle Actuator': '4C',
  'Warm-ups Since Codes Cleared': '30',
  'Fuel Rail Pressure': '22',
  'Fuel Rail Absolute Pressure': '59',
  'Time Since Trouble Codes Cleared': '4E',
  'Commanded EGR': '2C',
  'Ethanol Fuel Percent': '52',
  'Engine Reference Torque': '63',
  'Time Run With MIL On': '4D',
  'Fuel Pressure': '0A',
  'Absolute Load Value': '43',
  'Absolute Throttle Position B': '47',
  'Absolute Throttle Position C': '48',
  'Monitor Status This Drive Cycle': '41',
  'Control Module Voltage': '42',
  'Absolute Barometric Pressure': '33',
  'Relative Throttle Position': '45',
  'MAF Air Flow Rate': '10',
  'Fuel Rail Gauge Pressure': '23',
  'Catalyst Temperature: Bank 2, Sensor 1': '3D',
  'Catalyst Temperature: Bank 2, Sensor 2': '3F',
  'Timing Advance': '0E',
  'Short Term Fuel Trim-Bank 1': '06',
  'Short Term Fuel Trim-Bank 2': '08',
  'Fuel Tank Level Input': '2F',
  'Distance Traveled With Malfunction Indicator Lamp (MIL) On': '21',
  'Commanded Evaporative Purge': '2E',
  'Engine Oil Temperature': '5C',
  'EGR Error': '2D',
}

def decode(rawData):
    global OBD_DICT, OBD_LOG, OBD_FUNC, obd_string, i
    
    OBD_LEN = 1
    command = rawData[0]
    command_breakdown = command.split()
    for i in range(1,len(command_breakdown)):
        obd_command_len = OBD_DICT[command_breakdown[i]]
        OBD_LEN = OBD_LEN + obd_command_len + 1
    
    option_1 = 0
    for i in range(1,len(rawData)):
        if ':' in rawData[i]:
            option_1 = 1
        
    a=''
    b=''
    c=''
    if (option_1 == 1):
        for i in range(1,len(rawData)):
            if '0:' in rawData[i]:
                a = rawData[i]
                if (len(a) < 20):
                    a = a + rawData[i+1]
                a = a.replace('0: ','')
            if '1:' in rawData[i]:
                b = rawData[i]
                if (len(b) < 20):
                    b = b + rawData[i+1]
                b = b.replace('1: ','')
            if '2:' in rawData[i]:
                c = rawData[i]
                if (len(c) < 20):
                    c = c + rawData[i+1]
                c = c.replace('2: ','')
            if (len(a) > 2 and len(b) > 2 and len(c) > 2):
                break
    else:
        for i in range(1,len(rawData)):
            if '41' in rawData[i]:
                a = rawData[i]

    new_string = a+b+c
    new_string = new_string.replace('\n','')
    obd_string = new_string.split(' ')
    if (obd_string[-1] == "" or " "):
        obd_string.pop()
    obd_string = obd_string[:OBD_LEN]
    
    i = 1
    obd_cnt = 0
    while i < len(obd_string):
        obd_code_check = OBD_DICT.get(obd_string[i],0)
        if (obd_code_check == 0):
            break
        obd_code = OBD_DICT[obd_string[i]]
        if (obd_code != 0):
            obd_data = OBD_FUNC[obd_string[i]]()
            obd_cnt +=1
            #print(obd_data)
        if (obd_cnt == 6):
            break
        i += (obd_code+1)

def logging(gps, obdTime):
	global begin, fileName, log, stop, t2, camera, audio_proc, outfilenamevideo, outfilenameaudio, outfilenamemp3, encoded_filename, encoded_filename2, videoSetting
	sockets.on("start", start_handler)
	sockets.on("stop", stop_handler)
	if (begin == True):
		OBD_LOG['GPS'] = gps
		OBD_LOG['OBD Time'] = obdTime
		with open(str("logs/" + fileName + ".json"), 'a') as outfile:
			json.dump(OBD_LOG, outfile)
			if (stop == True):
				outfile.write(']')
				if(videoSetting == True):
					camera.stop_recording()
					audio_proc.kill()
					audio_proc=None
					subprocess.run(["lame", "-V2", outfilenameaudio, outfilenamemp3])
					subprocess.run(["MP4Box", "-add", outfilenamevideo,"-fps", "40", encoded_filename])
					subprocess.run(["ffmpeg", "-i", encoded_filename, "-i", outfilenamemp3, "-c","copy", "-map", "0:v:0", "-map", "1:a:0", encoded_filename2])
					t2.join()
				begin = False
			else:
				outfile.write(',')
		print("finished logging")

def record():
	global camera, audio_proc, outfilenamevideo, outfilenameaudio, outfilenamemp3, encoded_filename, encoded_filename2
	camera.resolution=(1280,720)
	camera.framerate=40
	timestamp = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
	outfilenamevideo="./video/output-"+timestamp+".h264"
	outfilenameaudio="./video/output-"+timestamp+".wav"
	outfilenamemp3="./video/output-"+timestamp+".mp3"
	audio_args=['arecord', '--device=hw:1,0', '-f', 'S16_LE', '-r', '44100', '-c1', outfilenameaudio]
	encoded_filename="./video/output-"+timestamp+".mp4"
	encoded_filename2="output_final-"+timestamp+".mp4"
	audio_proc=subprocess.Popen(audio_args, shell=False, preexec_fn=os.setsid)
	camera.start_recording(outfilenamevideo)

def video_handler(msg):
	global videoSetting
	print(msg)
	videoSetting = msg
	
def start_handler(msg):
	global begin, fileName, stop, t2, videoSetting, camera
	print('test: ', msg)
	begin = msg
	stop = False
	if (videoSetting == True):
		camera = picamera.PiCamera()
		t2 = threading.Thread(target=record)
		t2.start()
	fileName = str(datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S"))
	with open(str("logs/" + fileName + ".json"), 'a') as outfile:
		outfile.write('[')

def stop_handler(msg):
	global stop
	print('test: ', msg)
	stop = msg

def read():
	global response, OBDtime, newOBD, selectedCodesString
			
	while (1):
		input = selectedCodesString+'\r'
		sio.write(str(input))
		sio.flush()
		time.sleep(0.1)
		response = sio.readlines()
		newOBD = True
		OBDtime = datetime.datetime.now().isoformat()
		
def selectedCodes_handler(msg):
	global selectedCodes, selectedCodesString
	print(msg)
	selectedCodesString = "01"
	selectedCodes[msg['listID']] = msg['data']
	for i in range(len(selectedCodes)):
		if(selectedCodes[i] != ""):
			selectedCodesString += " "
			selectedCodesString += OBD_CODES[selectedCodes[i]]
			
def readGPS():
	global GPSData, newGPS, myGPS
	while(1):
		myGPS.read()

		#print myGPS.NMEA1
		#print myGPS.NMEA2

		if myGPS.fix != 0:
			data = {
				"UTC": myGPS.timeUTC,
				"satsTracked": myGPS.sats,
				"latitude":
				[{
					"degrees": myGPS.latDeg,
					"minutes": myGPS.latMin,
					"hemisphere": myGPS.latHem
				}],
				 "longitude":
				[{
					"degrees": myGPS.lonDeg,
					"minutes": myGPS.lonMin,
					"hemisphere": myGPS.lonHem
				}],
				"knots": myGPS.knots,
				"altitude": myGPS.altitude,
			}
			GPSData = data
			newGPS = True
	
	
def loop():
	global response, begin, stop, OBDtime, newOBD, GPSData, newGPS, myGPS, selectedCodesString
	data = ""
	gps = ""
	init()
	t1 = threading.Thread(target=readGPS)
	t1.start()
	sockets.on("selectedCodes", selectedCodes_handler)
	sockets.on("backendVideoSettings", video_handler)
	while(selectedCodes == ["","","","","",""]):
		print("waiting for user selection")
		time.sleep(6)
	t3 = threading.Thread(target=read)
	t3.start()
	while (1):
		if(newGPS == True):
			#print (GPSData)
			gps = GPSData
			newGPS = False
		if (newOBD == True):
			print(response)
			decode(response)
			data = json.dumps(OBD_LOG)
			print(data)
			sockets.emit('obd-in', data)
			newOBD = False
		logging(gps, OBDtime)
		time.sleep(0.1)

if __name__ == '__main__':
	try:
		loop()
	except KeyboardInterrupt:
		print("Exiting...")