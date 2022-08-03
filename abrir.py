file_path = 'datos.txt'

file_text = open(file_path, "r")

a = True

file_line = file_text.readline()
print(file_line)
x1=int(file_line[3:])
x1+=50
print(x1)


file_text.close()
