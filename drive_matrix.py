import smbus
import time
import numpy as np

DEVICE = 0x20

IODIRA = 0x00
IODIRB = 0x01

GPIOA = 0x12
GPIOB = 0x13


bus = smbus.SMBus(1)
a = np.ones([2,3])


#we set the direction of all GPIOs to 'output'
bus.write_byte_data(DEVICE, IODIRA, 0x00)
bus.write_byte_data(DEVICE, IODIRB, 0x00)

bus.write_byte_data(DEVICE, GPPUA, 0x00)
bus.write_byte_data(DEVICE, GPPUB, 0x00)

# 1 means that the corresponding LED is ON
# 0 means the the corresponding LED is OFF
# for each of the numbers below, the first list of the bigger list is the first row of LEDs, and so on

zero = [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]]
one = [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]
two = [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]]
three = [[1, 1, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]]
four = [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]]
five = [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]]
six = [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]]
seven = [[1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]]
eight = [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]]
nine = [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]]

digits = [one, two, three, four, five, six, seven, eight, nine]

#we sequentially light up each 'pixel' of the digitmatrix

#this function takes the digitmatrix and returns the data to send to MCP23017
def decode_digitmatrix_to_expanderdata(digitmatrix):
#	dataA = []
#	dataB = []
	#for each pixel of the digitmatrix we send a byte to bankA and a byte to bankB
	for irow, valr  in enumerate(digitmatrix):
		for icol, valc in enumerate(valr):
#			A = [0, 0, 0, 0, 0, 0, 0, 0] #data to send to bank A of MCP23017, the rightmost bit maps to GPA-0
#			B = [0, 0, 0, 0, 0, 0, 0, 0] #same for bank B
			if( valc == 1 ):
				bus.write_byte_data( DEVICE, GPIOA, 0b00000000 )
				A = [0, 0, 0, 0, 0, 0, 0, 0]
				A[7-icol] = 1 #cathode set to HIGH
				B = [1, 1, 1, 1, 1, 1, 1, 1]
				B[7-irow]=0   #anode set to LOW (that's the equivalent of GND)
				bus.write_byte_data(DEVICE, GPIOB, int(''.join(str(e) for e in B), 2))
				bus.write_byte_data(DEVICE, GPIOA, int(''.join(str(e) for e in A), 2))
				time.sleep(0.00001)
			#dataA.append(A)
			#dataB.append(B)
			#if((1 in A) or (1 in B)):
#				dataB.append(int(''.join(str(e) for e in B), 2))
#				dataA.append(int(''.join(str(e) for e in A), 2))
#				for k in range(5):
#					dataA.append(int("00000000",2))
#					dataB.append(int("00000000",2))
#				A[7-icol] = 0
#				dataA.append(int(''.join(str(e) for e in A), 2))
#				dataB.append(int(''.join(str(e) for e in B), 2))
#				dataA.append(int("00000000", 2))
#				dataB.append(int("00000000", 2))
#	return dataA, dataB

def send_data_to_expander(dataA, dataB, speed, duration):
	while(duration):
		for i in range(len(dataA)):
			bus.write_byte_data(DEVICE, GPIOA, dataA[i])
			bus.write_byte_data(DEVICE, GPIOB, dataB[i])
			time.sleep(speed)
#			bus.write_byte_data(DEVICE, GPIOA, 0b00000111)
#			bus.write_byte_data(DEVICE, GPIOB, 0b00011111)
#			time.sleep(0.001)
		duration -= 1


speed = 0.00001
duration = 100

#digit = raw_input("Enter a digit in letters : ")

#if(digit == "one"):
#data = decode_digitmatrix_to_expanderdata(one)
#send_data_to_expander(data[0], data[1], speed, duration)

for l in digits:
	for k in range(duration):
		decode_digitmatrix_to_expanderdata(l)


"""
#if(digit == "two"):
data = decode_digitmatrix_to_expanderdata(two)
send_data_to_expander(data[0], data[1], speed, duration)

#if(digit == "three"):
data = decode_digitmatrix_to_expanderdata(three)
send_data_to_expander(data[0], data[1], speed, duration)

#if(digit == "four"):
data = decode_digitmatrix_to_expanderdata(four)
send_data_to_expander(data[0], data[1], speed, duration)

#if(digit == "five"):
data = decode_digitmatrix_to_expanderdata(five)
send_data_to_expander(data[0], data[1], speed, duration)

#if(digit == "six"):
data = decode_digitmatrix_to_expanderdata(six)
send_data_to_expander(data[0], data[1], speed, duration)

#if(digit == "seven"):
data = decode_digitmatrix_to_expanderdata(seven)
send_data_to_expander(data[0], data[1], speed, duration)

#if(digit == "eight"):
data = decode_digitmatrix_to_expanderdata(eight)
send_data_to_expander(data[0], data[1], speed, duration)

#if(digit == "nine"):
data = decode_digitmatrix_to_expanderdata(nine)
send_data_to_expander(data[0], data[1], speed, duration)

"""

"""
for i in data[0]:
	print(i)

print('\n')

for i in data[1]:
	print(i)
"""

#send_data_to_expander(data[0], data[1], 0.01, 10)




"""
for i in range(100000):
	bus.write_byte_data(DEVICE, GPIOA, 0b00000100)
	bus.write_byte_data(DEVICE, GPIOB, 0b00000000)
	time.sleep(0.00001)

	bus.write_byte_data(DEVICE, GPIOA, 0b00000010)
	bus.write_byte_data(DEVICE, GPIOB, 0b00000000)
	time.sleep(0.00001)

	bus.write_byte_data(DEVICE, GPIOA, 0b00000111)
	bus.write_byte_data(DEVICE, GPIOB, 0b00000010)
	time.sleep(1)

	bus.write_byte_data(DEVICE, GPIOA, 0b00000000)
	bus.write_byte_data(DEVICE, GPIOB, 0b00000000)
	time.sleep(1)
"""

bus.write_byte_data(DEVICE, GPIOA, 0b00000000)
bus.write_byte_data(DEVICE, GPIOB, 0b00000000)
