"""
Script for driving a LED marix with a raspberry pi.
The LEDMatrix is handmade by soldering 3mm LEDs and resistors
The matrix is connected to the raspberry pi through a GPIO expander MCP23017.
The GPIO expander MCP23017 communicates with the raspberry pi through the I2C bus.
"""
import time
import smbus
bus = smbus.SMBus(1)

DEVICE = 0x20 #@ of MCP23017 in the I2C bus
IODIRA = 0x00
IODIRB = 0x01
GPIOA = 0x12
GPIOB = 0x13
#we set the direction of all GPIOs to 'output'
bus.write_byte_data(DEVICE, IODIRA, 0x00)
bus.write_byte_data(DEVICE, IODIRB, 0x00)

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

digits = [zero, one, two, three, four, five, six, seven, eight, nine]

#we sequentially light up each 'pixel' of the digitmatrix
#this function takes the digitmatrix and returns the data to send to MCP23017
def decode_digitmatrix_to_expanderdata(digitmatrix):
	#for each pixel of the digitmatrix we send a byte to bankA and a byte to bankB
	for irow, valr  in enumerate(digitmatrix):
		for icol, valc in enumerate(valr):
			if( valc == 1 ):
				bus.write_byte_data( DEVICE, GPIOA, 0b00000000 )
				A = [0, 0, 0, 0, 0, 0, 0, 0]
				A[7-icol] = 1 #cathode set to HIGH
				B = [1, 1, 1, 1, 1, 1, 1, 1]
				B[7-irow]=0   #anode set to LOW (that's the equivalent of GND)
				bus.write_byte_data(DEVICE, GPIOB, int(''.join(str(e) for e in B), 2))
				bus.write_byte_data(DEVICE, GPIOA, int(''.join(str(e) for e in A), 2))
				time.sleep(0.00001)

"""
attributes: size for example (3,5)

there should be 3 functions:
character2Matrix : represents an alphanumeral as a matrix of 0s and 1s where 0: led off, 1: led on
encode_character : takes an alphanumeral and returns a sequence of 16 bits
write : sends the sequence of bits to the ledmatrix

Actually, there should a base class and derived classes for each matrix size:
write -> base class
character2Matrix, encode_character -> derived class
"""

if __name__=='__main__':
	duration = 100
	for l in digits:
		for k in range(duration):
			decode_digitmatrix_to_expanderdata(l)

#Setting LED matrix to OFF
bus.write_byte_data(DEVICE, GPIOA, 0b00000000)
bus.write_byte_data(DEVICE, GPIOB, 0b00000000)
