from machine import I2C
from hmc5883l import HMC5883L
from time import sleep

# Please check that correct PINs are set on hmc5883l library!
sensor = HMC5883L()
while True:
    sleep(1)
    x, y, z = sensor.read()
    print(sensor.format_result(x, y, z))
