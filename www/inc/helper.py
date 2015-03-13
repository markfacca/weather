

class Convert:

	def __init__(self):
		#nothinghere
		pass

	@staticmethod
	def TempFtoC(fTemp):
		convVal = ((fTemp - 32) * float(5)) / float(9)
		return convVal
		
	
			
class Validation:
	@staticmethod
	def CheckNull(inputVariable, defaultValue=''):
		if inputVariable is None:
			return defaultValue
		else:
			return inputVariable
			

