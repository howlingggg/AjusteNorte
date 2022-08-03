import machine
import utime

boton = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)


while True:
    if boton.value() == 1:
        print("iniciando secuencia de calibracion: ")
        utime.sleep(2)
        import HMC5882Lcalibration
        utime.sleep(2)
        continue
