import serial # 安装pyserial，但import serial，且不能安装serial

# ser为串口对象，后续调用均用点运算符
ser = serial.Serial('/dev/ttyUSB0', 115200) # 'COM7', 3000000, bytesize=8, parity='N', stopbits=1
ser.write("$KMS:-100,200,200,3000!".encode('utf-8'))