import serial
import json
from time import sleep

ser = serial.Serial('/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_01C72E85-if00-port0',9600)

class GPS:
	def __init__(self):
		UPDATE_10_sec=  "$PMTK220,10000*2F\r\n"       #Update Every 10 Seconds
		UPDATE_5_sec=  "$PMTK220,5000*1B\r\n"         #Update Every 5 Seconds  
		UPDATE_1_sec=  "$PMTK220,1000*1F\r\n"         #Update Every One Second
		UPDATE_200_msec=  "$PMTK220,200*2C\r\n"       #Update Every 200 Milliseconds
		UPDATE_100_msec=  "$PMTK220,100*2F\r\n"       #Update Every 100 Milliseconds
		MEAS_10_sec = "$PMTK300,10000,0,0,0,0*2C\r\n" #Measure every 10 seconds
		MEAS_5_sec = "$PMTK300,5000,0,0,0,0*18\r\n"   #Measure every 5 seconds
		MEAS_1_sec = "$PMTK300,1000,0,0,0,0*1C\r\n"   #Measure once a second
		MEAS_200_msec= "$PMTK300,200,0,0,0,0*2F\r\n"  #Measure 5 times a second
		MEAS_100_msec= "$PMTK300,100,0,0,0,0*2F\r\n"  #Measure 10 times a second
		
		BAUD_57600 = "$PMTK251,57600*2C\r\n"          #Set Baud Rate at 57600
		BAUD_9600 ="$PMTK251,9600*17\r\n"             #Set 9600 Baud Rate
		WAAS_Search ="$PMTK501,2*28\r\n"             #force enable WAAS search
		
		ser.write(str.encode(BAUD_57600))
		sleep(1)
		
		ser.baudrate=57600
		
		GPRMC_ONLY= "$PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29\r\n"  #Send only the GPRMC Sentence
		GPRMC_GPGGA="$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n"  #Send GPRMC AND GPGGA Sentences
		SEND_ALL ="$PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n"    #Send All Sentences
		SEND_NOTHING="$PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28\r\n" #Send Nothing
		
		ser.write(str.encode(UPDATE_100_msec))
		sleep(1)
		
		ser.write(str.encode(MEAS_100_msec))
		sleep(1)
		
		ser.write(str.encode(WAAS_Search))
		sleep(1)
		
		ser.write(str.encode(GPRMC_GPGGA)) #We can get away with just GPGGA but GPRMC is helpful, too
		sleep(1)
		
		ser.flushInput()
		ser.flushInput()
		
		#print "GPS Initialized"
                
	def read(self):
		ser.flushInput()
		ser.flushInput()
		
		while ser.inWaiting()==0:
				pass
		self.NMEA1=ser.readline()
		
		while ser.inWaiting()==0:
				pass
		self.NMEA2=ser.readline()
		
		NMEA1_array=self.NMEA1.decode().split(',')
		NMEA2_array=self.NMEA2.decode().split(',')
		
		#The NMEA sentnces appear to come in in different orders; check both possibilities
		
		if NMEA1_array[0] == '$GPRMC':
				self.timeUTC  = NMEA1_array[1][:-8]+':'+NMEA1_array[1][-8:-6]+':'+NMEA1_array[1][-6:]
				self.latDeg   = NMEA1_array[3][:-7]
				self.latMin   = NMEA1_array[3][-7:]
				self.latHem   = NMEA1_array[4]
				self.lonDeg   = NMEA1_array[5][:-7]
				self.lonMin   = NMEA1_array[5][-7:]
				self.lonHem   = NMEA1_array[6]
				self.knots    = NMEA1_array[7]
				
		if NMEA1_array[0] == '$GPGGA':
				self.fix      = NMEA1_array[6]
				self.altitude = NMEA1_array[9]
				self.sats     = NMEA1_array[7]
				
		if NMEA2_array[0] == '$GPRMC':
				self.timeUTC  = NMEA2_array[1][:-8]+':'+NMEA1_array[1][-8:-6]+':'+NMEA1_array[1][-6:]
				self.latDeg   = NMEA2_array[3][:-7]
				self.latMin   = NMEA2_array[3][-7:]
				self.latHem   = NMEA2_array[4]
				self.lonDeg   = NMEA2_array[5][:-7]
				self.lonMin   = NMEA2_array[5][-7:]
				self.lonHem   = NMEA2_array[6]
				self.knots    = NMEA2_array[7]

		if NMEA2_array[0] == '$GPGGA':
				self.fix      = NMEA2_array[6]
				self.altitude = NMEA2_array[9]
				self.sats     = NMEA2_array[7]