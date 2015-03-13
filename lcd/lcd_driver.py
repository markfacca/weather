import serial
import array


class LCD:
	def __init__(self):
		pass
		
	def Connect(self, device):
		try:
			self.serialComm = serial.Serial(device, baudrate=19200, timeout=3.0)
		except serial.SerialException as x:
			print "Serial port open error: " + x.__str__()
			exit(1)
			
	def ClearScreen(self):
		self.serialComm.write(LCDCmd.CLEAR_SCREEN)
		pass
		
	def InitialSetup(self):
		
		#Define custom character bitmaps
		customChar1 = bytearray(b'\x02\x05\x05\x02\x00\x00\x00\x00')
		
		self.SetCustomCharBitmap(0, customChar1)
		self.serialComm.write(LCDCmd.HIDE_CURSOR)
		self.serialComm.write(LCDCmd.SET_CONTRAST + chr(10))
		self.serialComm.write(LCDCmd.SET_BRIGHTNESS + chr(60))
		self.ClearScreen()
		pass
		
	def WriteString(self, col, row, text):
		self.MoveCursor(col,row)
		self.serialComm.write(text)
		pass
		
	def MoveCursor(self, col, row):
		self.serialComm.write(LCDCmd.MOVE_CURSOR + chr(col) + chr(row))
		pass
		
	def SetCustomCharBitmap(self, charId, bitmapData):
		self.serialComm.write(LCDCmd.SET_CUSTOM_CHAR_BITMAP + chr(charId) + bitmapData)
		
	def Test1(self):
		self.serialComm.write(chr(22) + chr(255) + chr(5) + chr(20))

class LCDCmd:
	CLEAR_SCREEN 				= bytearray(b'\x0C')
	HIDE_CURSOR					= bytearray(b'\x04')
	SET_CONTRAST				= bytearray(b'\x0E')
	SET_BRIGHTNESS				= bytearray(b'\x0F')
	MOVE_CURSOR					= bytearray(b'\x11')
	SET_CUSTOM_CHAR_BITMAP		= bytearray(b'\x19')




