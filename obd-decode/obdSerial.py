import time
import serial
import io
import socketio
import threading
import json
import datetime
import os

begin = False
stop = False
newOBD = False
initialBegin = False
obd_string = ""
i= 0
OBDtime = ""
log = {}
fileName = ""
response = []
VIN = ""
t2= ""
possibleCodes= []
selectedCodes = ""

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
	if(os.path.exist('profiles/'+VIN+'.txt')):
		f = open('profiles/'+VIN+'.txt')
		contents = f.read()
		print(contents)
		possibleCodes = contents
		sockets.emit('possibleCodes', possibleCodes)
		f.close()
		#need to figure out where we want to convert codes to string
	else:
		possibleCodes = possibleCodesScan()
		print(possibleCodes)
		f = open('profiles/'+VIN+'.txt',"w+")
		f.write(possibleCodes)
		sockets.emit('possibleCodes', possibleCodes)
		f.close()
		
def possibleCodesScan():
	work = []
	dontwork = []
	for i in range(0, len(codes)):
		input = "01" + OBD_CODES[i] + "\r"
		sio.write(unicode(input))
		sio.flush()
		time.sleep(0.2)
		response = sio.readlines()
		print(response)
		for j in range(0,len(response)):
			if j == 1:
				if(response[j] != u'NO DATA\n'):
					work.append(OBD_CODES[i])
				else:
					dontwork.append(OBD_CODES[i])

	print("Scan is complete")
	return work

def CEL_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = float(100/255)*A
    OBD_LOG['Calculated Engine Load'] = OBD_data

def ECT_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = A - 40
    OBD_LOG['Engine coolant temperature'] = OBD_data

def STFTB1_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = (float(100/255)*A) - 100
	OBD_LOG['Short term fuel trim - Bank 1'] = OBD_data
	
def LTFTB1_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = (float(100/255)*A) - 100
	OBD_LOG['Long term fuel trim - Bank 1'] = OBD_data
	
def STFTB2_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = (float(100/255)*A) - 100
	OBD_LOG['Short term fuel trim - Bank 2'] = OBD_data
	
def LTFTB2_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = (float(100/255)*A) - 100
	OBD_LOG['Long term fuel trim - Bank 2'] = OBD_data
	
def RPM_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A+B)/4
    OBD_LOG['Engine RPM'] = OBD_data
    
def MPH_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = int(A*(.621))
    OBD_LOG['Vehicle Speed'] = OBD_data
    
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

def OSVSTFTB2_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = A/200
	OBD_data_2 = (float(100/128)*B)-100
	OBD_LOG['Oxygen Sensor 2: Voltage'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 2: Short Term Fuel Trim'] = OBD_data_2
	
def OSVSTFTB6_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = A/200
	OBD_data_2 = (float(100/128)*B)-100
	OBD_LOG['Oxygen Sensor 6: Voltage'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 6: Short Term Fuel Trim'] = OBD_data_2
	
def OSVSTFTB7_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data_1 = A/200
	OBD_data_2 = (float(100/128)*B)-100
	OBD_LOG['Oxygen Sensor 7: Voltage'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 7: Short Term Fuel Trim'] = OBD_data_2	

def RTSES_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A)+B
    OBD_LOG['Run time since engine start'] = OBD_data
	
def DTWMILO_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A)+B
    OBD_LOG['Distance traveled with malfunction indicator lamp (MIL) on'] = OBD_data

def OSABCDFAERVB1_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = float(2/65536)*(256*A+B)
	OBD_data_2 = float(8/65536)*(256*C+D)
	OBD_LOG['Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 1 CD: Voltage'] = OBD_data_2

def OSABCDFAERVB5_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = float(2/65536)*(256*A+B)
	OBD_data_2 = float(8/65536)*(256*C+D)
	OBD_LOG['Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 1 CD: Voltage'] = OBD_data_2

def OSABCDFAERVB6_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = float(2/65536)*(256*A+B)
	OBD_data_2 = float(8/65536)*(256*C+D)
	OBD_LOG['Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 1 CD: Voltage'] = OBD_data_2
	
def OSABCDFAERVB8_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = float(2/65536)*(256*A+B)
	OBD_data_2 = float(8/65536)*(256*C+D)
	OBD_LOG['Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 1 CD: Voltage'] = OBD_data_2
	
def CEP_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = float(100/255)*A
    OBD_LOG['Commanded Evaporative Purge'] = OBD_data
	
def WUSCC_Decode():
    A = int(obd_string[i+1],16)
    OBD_data = A
    OBD_LOG['Warm-ups since codes cleared'] = OBD_data

def DTSCC_Decode():
    A = int(obd_string[i+1],16)
    B = int(obd_string[i+2],16)
    OBD_data = (256*A+B)
    OBD_LOG['Distance traveled since codes cleared'] = OBD_data
	
def ABP_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = A
	OBD_LOG['Absolute Barometric Pressure'] = OBD_data
	
def OSABCDFAERCB1_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = float(2/65536)*(256*A+B)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 1 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 1 CD: Voltage'] = OBD_data_2

def OSABCDFAERCB2_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = float(2/65536)*(256*A+B)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 2 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 2 CD: Voltage'] = OBD_data_2

def OSABCDFAERCB4_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = float(2/65536)*(256*A+B)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 4 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 4 CD: Voltage'] = OBD_data_2
	
def OSABCDFAERCB5_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = float(2/65536)*(256*A+B)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 5 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 5 CD: Voltage'] = OBD_data_2

def OSABCDFAERCB6_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = float(2/65536)*(256*A+B)
	OBD_data_2 = C + (D/256) - 128
	OBD_LOG['Oxygen Sensor 6 AB: Fuel-Air Equivalence Ratio 2'] = OBD_data_1
	OBD_LOG['Oxygen Sensor 6 CD: Voltage'] = OBD_data_2

def OSABCDFAERCB8_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data_1 = float(2/65536)*(256*A+B)
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
	OBD_LOG['Control module voltage'] = OBD_data
	
def ALV_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = float(100/255)*(256*A+B)
	OBD_LOG['Absolute load value'] = OBD_data
	
def FACER_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = float(2/65536)*(256*A+B)
	OBD_LOG['Fuel-Air commanded equivalence ratio'] = OBD_data
	
def RTP_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = float(100/255)*A
	OBD_LOG['Relative throttle position'] = OBD_data
	
def ATPB_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = float(100/255)*A
	OBD_LOG['Absolute throttle position B'] = OBD_data

def APPD_Decode(): 
	A = int(obd_string[i+1],16)
	OBD_data = float(100/255)*A
	OBD_LOG['Absolute throttle position D'] = OBD_data
	
def APPE_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = float(100/255)*A
	OBD_LOG['Absolute throttle position E'] = OBD_data
	
def CTA_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = float(100/255)*A
	OBD_LOG['Commanded throttle actuator'] = OBD_data
	
def TRWMILO_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = (256*A+B)
	OBD_LOG['Time run with MIL on'] = OBD_data
	
def TSTCC_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = float(2/65536)*(256*A+B)
	OBD_LOG['Time since trouble codes cleared'] = OBD_data

def MVFFAEROSVOSCAIMAP_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data = 10*D
	OBD_LOG['Maximum value for Fuel-Air equivalence ratio'] = A
	OBD_LOG['Maximum value for oxygen sensor voltage'] = B
	OBD_LOG['Maximum value for oxygen sensor current'] = C
	OBD_LOG['Maximum value for intake manifold absolute pressure'] = OBD_data

def MVFAFRFMAFS_Decode():
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	C = int(obd_string[i+2],16)
	D = int(obd_string[i+2],16)
	OBD_data = 10*A
	OBD_LOG['Maximum value for air flow from mass air flow sensor'] = A

def EF_Decode(): 
	A = int(obd_string[i+1],16)
	OBD_data = float(100/255)*A
	OBD_LOG['Ethanol fuel %'] = OBD_data

def AESVP_Decode(): 
	A = int(obd_string[i+1],16)
	B = int(obd_string[i+2],16)
	OBD_data = ((256*A+B)/200)
	OBD_LOG['Absolute Evap system Vapor Pressure'] = OBD_data
	
def AEPT_Decode():
	A = int(obd_string[i+1],16)
	OBD_data = A-125
	OBD_LOG['Actual engine - percent torque'] = OBD_data
	
OBD_DICT = {'00' : 0,'04' : 1,'05' : 1,'06' : 1,'07' : 1,'08' : 1,'09' : 1,'0C' : 2,'0D' : 1,'0E' : 1,'0F' : 1,'10' : 2,'11' : 1,'15' : 2,'19' : 2,'1A' : 2,'1F' : 2,'21' : 2,'24' : 4,'28' : 4,'29' : 4,'2B' : 4,'2E' : 1,'30' : 1,'31' : 2,'33' : 1,'34' : 4,'35' : 4,'37' : 4,'38' : 4,'39' : 4,'3B' : 4,'3C' : 2,'3D' : 2,'3E' : 2,'3F' : 2,'42' : 2,'43' : 2,'44' : 2,'45' : 1,'47' : 1,'49' : 1,'4A' : 1,'4C' : 1,'4D' : 2,'4E' : 2,'4F' : 4,'50' : 4,'52' : 1,'53' : 2,'62' : 1}
OBD_LOG = {}
OBD_FUNC = {'04' : CEL_Decode,'05' : ECT_Decode,'06' : STFTB1_Decode,'07' : LTFTB1_Decode,'08' : STFTB2_Decode,'09' : LTFTB2_Decode,'0C' : RPM_Decode,'0D' : MPH_Decode,'0E' : TA_Decode,'0F' : IAT_Decode,'10' : MAFAFR_Decode,'11' : TP_Decode,'15' : OSVSTFTB2_Decode,'19' : OSVSTFTB6_Decode,'1A' : OSVSTFTB7_Decode,'1F' : RTSES_Decode,'21' : DTWMILO_Decode,'24' : OSABCDFAERVB8_Decode,'28' : OSABCDFAERVB5_Decode,'29' : OSABCDFAERVB6_Decode,'2B' : OSABCDFAERVB8_Decode,'2E' : CEP_Decode,'30' : WUSCC_Decode,'31' : DTSCC_Decode,'33' : ABP_Decode,'34' : OSABCDFAERCB1_Decode,'35' : OSABCDFAERCB2_Decode,'37' : OSABCDFAERCB4_Decode,'38' : OSABCDFAERCB5_Decode,'39' : OSABCDFAERCB6_Decode,'3B' : OSABCDFAERCB8_Decode,'3C' : CTB1S1_Decode,'3D' : CTB2S1_Decode,'3E' : CTB1S2_Decode,'3F' : CTB2S2_Decode,'42' : CMV_Decode,'43' : ALV_Decode,'44' : FACER_Decode,'45' : RTP_Decode,'47' : ATPB_Decode,'49' : APPD_Decode,'4A' : APPE_Decode,'4C' : CTA_Decode,'4D' : TRWMILO_Decode,'4E' : TSTCC_Decode,'4F' : MVFFAEROSVOSCAIMAP_Decode,'50' : MVFAFRFMAFS_Decode,'52' : EF_Decode,'53' : AESVP_Decode,'62' : AEPT_Decode}
OBD_CODES = ["00","01","02","03","04","05","06","07","08","09","0A","0B","0C","0D","0E","0F","1","10","11","12","13","14","15","16","17","18","19","1A","1B","1C","1D","1E","1F","2","20","21","22","23","24","25","26","27","28","29","2A","2B","2C","2D","2E","2F","3","30","31","32","33","34","35","36","37","38","39","3A","3B","3C","3D","3E","3F","4","40","41","42","43","44","45","46","47","48","49","4A","4B","4C","4D","4E","4F","5","50","51","52","53","54","55","56","57","58","59","5A","5B","5C","5D","5E","5F","6","60","61","62","63","64","65","66","67","68","69","6A","6B","6C","6D","6E","6F","7","70","71","72","73","74","75","76","77","78","79","7A","7B","7C","7D","7E","7F","8","80","81","82","83","84","85","86","87","88","89","8A","8B","8C","8D","8E","8F","9","90","91","92","93","94","98","99","9A","9B","9C","9D","9E","9F","A0","A1","A2","A3","A4","A5","A6","C0","C3","C4"]
def decode(rawData):
	global OBD_DICT, OBD_LOG, OBD_FUNC, obd_string, i
	
	a=''
	b=''
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
		if (len(a) > 2 and len(b) > 2):
			break

	new_string = a+b
	new_string = new_string.replace('\n','')
	obd_string = new_string.split(' ')
	if (obd_string[-1] == "" or " "):
		obd_string.pop()

	i = 1
	obd_cnt = 0
	while i < len(obd_string):
		obd_code = OBD_DICT[obd_string[i]]
		if (obd_code != 0):
			obd_data = OBD_FUNC[obd_string[i]]()
			obd_cnt +=1
			#print(obd_data)
		if (obd_cnt == 5):
			break
		i += (obd_code+1)

def logging(gps, obdTime):
    global begin, fileName, log, stop, t2
    sockets.on("start", message_handler)
    sockets.on("stop", stop_handler)
    if (begin == True):
        OBD_LOG['GPS'] = gps
        OBD_LOG['OBD Time'] = obdTime
        with open(str(fileName + ".json"), 'a') as outfile:
            json.dump(OBD_LOG, outfile)
            if (stop == True):
                outfile.write(']')
                os.system("sudo killall ffmpeg")
                begin = False
				t2.join()
            else:
                outfile.write(',')
    	print("finished logging")

def record():
	os.system("recordvideo")
	
def message_handler(msg):
	global begin, fileName, stop, t2
	print('test: ', msg)
	begin = msg
	stop = False
	t2 = threading.Thread(target=record)
	t2.start()
	fileName = str(datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S"))
	with open(str(fileName + ".json"), 'a') as outfile:
		outfile.write('[')

def stop_handler(msg):
	global stop
	print('test: ', msg)
	stop = msg

def read():
	global response, OBDtime, newOBD, selectedCodes
	while (1):
		input = selectedCodes+'\r'
		sio.write(str(input))
		sio.flush()
		time.sleep(0.1)
		response = sio.readlines()
		newOBD = True
		OBDtime = datetime.datetime.now().isoformat()
		
def selectedCodes_handler(msg):
	global selectedCodes
	selectedCodes = msg
	
def loop():
	global response, begin, stop, OBDtime, newOBD
	data = ""
	init()
	sockets.on("selectedCodes", selectedCodes_handler)
	while(selectedCodes == ""):
		print("waiting for user selection")
	t1 = threading.Thread(target=read)
	t1.start()
	while (1):
		gps = datetime.datetime.now().isoformat() #go get GPS data
		time.sleep(0.1)
		if (newOBD == True):
			print(response)
			print(datetime.datetime.now().isoformat())
			decode(response)
			data = json.dumps(OBD_LOG)
			sockets.emit('obd-in', data)
			newOBD = False
		logging(gps, OBDtime)

if __name__ == '__main__':
	try:
		loop()
	except KeyboardInterrupt:
		print("Exiting...")