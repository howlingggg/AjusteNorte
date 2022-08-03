import utime
from machine import I2C, Pin
from mpu6500 import MPU6500

i2c = I2C(0,scl=Pin(1), sda=Pin(0))
sensor = MPU6500(i2c)

print("MPU9250 id: " + hex(sensor.whoami))

while True:
    print(sensor.acceleration)

    utime.sleep_ms(1000)