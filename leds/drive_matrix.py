"""
Script for driving a LED marix with a raspberry pi.
The LEDMatrix is handmade by soldering 3mm LEDs and resistors
The matrix is connected to the raspberry pi via a GPIO expander MCP23017.
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

# 1 means that the corresponding LED is ON
# 0 means the the corresponding LED is OFF
# for each of the numbers below, the first list of the bigger list is the first row of LEDs, and so on
digits = {
	0: [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
	1: [[0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
	2: [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
	3: [[1, 1, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
	4: [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
	5: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
	6: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
	7: [[1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
	8: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
	9: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]]
}

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


if __name__=='__main__':

	#we set the direction of all GPIOs to 'output'
	bus.write_byte_data(DEVICE, IODIRA, 0x00)
	bus.write_byte_data(DEVICE, IODIRB, 0x00)

	duration = 100 #adapt the duration to the number of leds set to ON
	for l in digits.keys():
		for k in range(duration):
			decode_digitmatrix_to_expanderdata(l)

	#Setting LED matrix to OFF
	bus.write_byte_data(DEVICE, GPIOA, 0b00000000)
	bus.write_byte_data(DEVICE, GPIOB, 0b00000000)
