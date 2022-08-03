
import utime
from machine import I2C
from hmc5883l import HMC5883L
from time import sleep

# Please check that correct PINs are set on hmc5883l library!
sensor = HMC5883L()

Xmin=1000
Xmax=-1000
Ymin=1000
Ymax=-1000

while True:
    contador = 0
    while contador < 15:
        sleep(0.2)
        x, y, z = sensor.read()
        Xmin=min(x,Xmin)
        Xmax=max(x,Xmax)
        Ymin=min(y,Ymin)
        Ymax=max(y,Ymax)
        print(sensor.format_result(x, y, z))
        print("Xmin="+str(Xmin)+"; Xmax="+str(Xmax)+"; Ymin="+str(Ymin)+"; Ymax="+str(Ymax))
        contador +=1
        sleep(0.2)
    else:
        print()
        xs=1
        ys=(Xmax-Xmin)/(Ymax-Ymin)
        xb =xs*(1/2*(Xmax-Xmin)-Xmax)
        yb =xs*(1/2*(Ymax-Ymin)-Ymax)
        print("Valores de calibracion:")
        print("xs="+str(xs))
        print("xb="+str(xb))
        print("ys="+str(ys))
        print("yb="+str(yb))
        break

