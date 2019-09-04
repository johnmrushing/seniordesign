import serial
import io

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=10000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.01,
)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
codes = ["00"]
    #,"01","02","03","04","05","06","07","08","09","0A","0B","0C","0D","0E","0F","1","10","11","12","13","14","15","16","17","18","19","1A","1B","1C","1D","1E","1F","2","20","21","22","23","24","25","26","27","28","29","2A","2B","2C","2D","2E","2F","3","30","31","32","33","34","35","36","37","38","39","3A","3B","3C","3D","3E","3F","4","40","41","42","43","44","45","46","47","48","49","4A","4B","4C","4D","4E","4F","5","50","51","52","53","54","55","56","57","58","59","5A","5B","5C","5D","5E","5F","6","60","61","62","63","64","65","66","67","68","69","6A","6B","6C","6D","6E","6F","7","70","71","72","73","74","75","76","77","78","79","7A","7B","7C","7D","7E","7F","8","80","81","82","83","84","85","86","87","88","89","8A","8B","8C","8D","8E","8F","9","90","91","92","93","94","98","99","9A","9B","9C","9D","9E","9F","A0","A1","A2","A3","A4","A5","A6","C0","C3","C4"]

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

for i in range(0, len(codes)):
    input = "01" + codes[i] + "\r"
    sio.write(unicode(input))
    sio.flush()
    time.sleep(1)
    response = sio.readlines()
    print(response)
    temp = ""



