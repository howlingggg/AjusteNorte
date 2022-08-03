f = open ('datos.txt','w')
f.write('x1=10 \n')
f.write('x2=45 \n')
f.write('x3=50 \n')
f.write('x4=60 \n')
f.close()


# archivo-entrada.py
file = open("datos.txt", "r")

while (f := file.read()):
    process(f)

file.close()
