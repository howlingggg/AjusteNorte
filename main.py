from machine import Pin, UART, I2C
import utime, time
from math import sqrt, atan2, pi, copysign, sin, cos
from mpu6500 import MPU6500
from time import sleep
from hmc5883l import HMC5883L
from micropyGPS import MicropyGPS
#https://github.com/inmcm/micropyGPS

led_1 = Pin(25, Pin.OUT)

blue = UART (0,9600) #Defino el modulo bluetooth en uart 0 (Rx 0 Tx 1)


#GPS Module UART Connection Conectar Rx a TX CRUZADOS!!!!
gps_module = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
TIMEZONE = -3
my_gps = MicropyGPS(TIMEZONE)
#__________________________________________________
sensor = HMC5883L()
#__________________________________________________
MPU = 0x68
id = 0
sda = Pin(16)
scl = Pin(17)
i2c = I2C(id=id, scl=scl, sda=sda)
m = MPU6500(i2c)
# _________________________________________________

def get_reading()->float:
    ''' Returns the readings from the sensor '''
    global filtered_y_value, filtered_x_value
    x = m.acceleration[0] 
    y = m.acceleration[1]
    z = m.acceleration[2] 
    roll_rad = atan2(-x, sqrt((z*z)+(y*y)))
    pitch_rad = atan2(z, copysign(y,y)*sqrt((0.01*x*x)+(y*y)))
    pitch = pitch_rad*180/pi -89.4  #Ajuste -89.4 para que al estar en horizontal Muestre 0º
    roll = roll_rad*180/pi +10
    return x, y, z, pitch, roll

def show():
    x, y, z, pitch, roll = get_reading()
    print("Pitch",round(pitch,1), "Roll",round(roll, 1))
    blue.write("Pitch: ""{:.2f}".format(pitch))
    blue.write(" ")
    blue.write("Roll: ""{:.2f}".format(roll))
    blue.write("\n")
    
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
        led_1.value(1)
        blue.write('Lat: N/A')
        blue.write(' \n')
        blue.write('Lng: N/A')
        blue.write(' \n')
        blue.write('Hora: N/A')
        blue.write(' ')
        blue.write('Fecha: N/A')
        blue.write(' \n')
        print("Sin Datos de satelite, espere...")
        show()
        x, y, z = sensor.read()
        print(sensor.format_result(x, y, z))
        blue.write(sensor.format_result(x, y, z))
        blue.write(' \n')
        time.sleep(1)
        led_1.value(0)
        if blue.any():
            msg = blue.readline()
            print(msg)
            if msg == b'calibrar\r\n': 
                print("Iniciando Calibracion")
                blue.write("Iniciando Calibracion \n")
                import HMC5882Lcalibration
                time.sleep(2)
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
    led_1.value(1)
    msg = blue.readline()
    print('Lat:', latitude)
    print('Lng:', longitude)
    print('Hora:', gpsTime)
    print('Fecha:', gpsdate)
    blue.write('Lat: '+str(latitude))
    blue.write(' \n')
    blue.write('Lng: '+str (longitude))
    blue.write(' \n')
    blue.write('Hora: '+str (gpsTime))
    blue.write(' ')
    blue.write('Fecha: '+str (gpsdate))
    blue.write(' \n')
    show()
    x, y, z = sensor.read()
    print(sensor.format_result(x, y, z))
    blue.write(sensor.format_result(x, y, z))
    blue.write(' \n')
    time.sleep(1)
    led_1.value(0)
    if blue.any():
        msg = blue.readline()
        print(msg)
        if msg == b'calibrar\r\n': 
            print("Iniciando Calibracion")
            blue.write("Iniciando Calibracion \n")
            import HMC5882Lcalibration
            time.sleep(2)
            continue
        else:
            continue
    continue
    #_________________________________________________