from machine import Pin, UART, I2C
import utime, time
from math import sqrt, atan2, pi, copysign, sin, cos
from mpu6500 import MPU6500
from time import sleep
from hmc5883l import HMC5883L
from micropyGPS import MicropyGPS
#https://github.com/inmcm/micropyGPS


boton = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)


#GPS Module UART Connection Conectar Rx a TX CRUZADOS!!!!
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
TIMEZONE = -3
my_gps = MicropyGPS(TIMEZONE)
#__________________________________________________
sensor = HMC5883L()
#__________________________________________________
MPU = 0x68
id = 0
sda = Pin(0)
scl = Pin(1)
i2c = I2C(id=id, scl=scl, sda=sda)
m = MPU6500(i2c)
filtered_x_value = 0.0 
filtered_y_value = 0.0
# _________________________________________________

def get_reading()->float:
    ''' Returns the readings from the sensor '''
    global filtered_y_value, filtered_x_value
    x = m.acceleration[0] 
    y = m.acceleration[1]
    z = m.acceleration[2] 

    # Pitch and Roll in Radians
    roll_rad = atan2(-x, sqrt((z*z)+(y*y)))
    pitch_rad = atan2(z, copysign(y,y)*sqrt((0.01*x*x)+(y*y)))

    # Pitch and Roll in Degrees
    pitch = pitch_rad*180/pi
    roll = roll_rad*180/pi
    return x, y, z, pitch, roll
def low_pass_filter(raw_value:float, remembered_value):
    ''' Only applied 20% of the raw value to the filtered value '''
    
    # global filtered_value
    alpha = 0.8
    filtered = 0
    filtered = (alpha * remembered_value) + (1.0 - alpha) * raw_value
    return filtered

def show():
    ''' Shows the Pitch, Rool and heading '''
    x, y, z, pitch, roll = get_reading()
    print("Pitch",round(pitch,1), "Roll",round(roll, 1))
    sleep(0.2)

# reset orientation to zero
x,y,z, pitch_bias, roll_bias = get_reading()



def convert(parts):
    if (parts[0] == 0):
        return None
        
    data = parts[0]+(parts[1]/60.0)
    # parts[2] contain 'E' or 'W' or 'N' or 'S'
    if (parts[2] == 'S'):
        data = -data
    if (parts[2] == 'W'):
        data = -data

    data = '{0:.6f}'.format(data) # to 6 decimal places
    return str(data)

while True:
    #_________________________________________________
    #print(i2c.scan())
    length = gps_module.any()
    if length>0:
        b = gps_module.read(length)
        for x in b:
            msg = my_gps.update(chr(x))
    #_________________________________________________
    latitude = convert(my_gps.latitude)
    longitude = convert(my_gps.longitude)
    #_________________________________________________
    if (latitude == None ):
        
        print("Sin Datos de satelite, espere...")
        show()
        x, y, z = sensor.read()
        print(sensor.format_result(x, y, z))
        time.sleep(2)
        if boton.value() == 1:
            print("Iniciando Calibracion")
            import HMC5882Lcalibration
            time.sleep(10)
            continue
        else:
            continue
        
        continue
    #_________________________________________________
    t = my_gps.timestamp
    #t[0] => hours : t[1] => minutes : t[2] => seconds
    gpsTime = '{:02d}:{:02d}:{:02}'.format(t[0], t[1], t[2])
    
    gpsdate = my_gps.date_string('long')
    speed = my_gps.speed_string('kph') #'kph' or 'mph' or 'knot'
    #_________________________________________________
    
    print('Lat:', latitude)
    print('Lng:', longitude)
    print('time:', gpsTime)
    print('Date:', gpsdate)
    show()
    x, y, z = sensor.read()
    print(sensor.format_result(x, y, z))
    time.sleep(2)
    
    if boton.value() == 1:
        print("Iniciando Calibracion")
        import HMC5882Lcalibration
        time.sleep(10)
        continue
    else:
        continue
    continue

    #_________________________________________________


