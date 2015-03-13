#!/usr/bin/python

class Output:

	def __init__(self):
		#nothinghere
		self.CurrentIndent = 0
		pass

	def Begin(self):
		#Reset buffer
		self.OutputBuffer = ""

	def Print(self, inputString, NewLine=True):
		#Add to string buffer
		if (NewLine == True):
			self.OutputBuffer += "\t" * self.CurrentIndent

		self.OutputBuffer += inputString
		
		if (NewLine == True):
			self.OutputBuffer += "\n"

	def Indent(self, tabCount=1):
		self.CurrentIndent += tabCount

	def Outdent(self, tabCount=1):
		if ((self.CurrentIndent - tabCount) >= 0 ):
			self.CurrentIndent -= tabCount
		else:
			self.CurrentIndent = 0

	def Finish(self):
		#Output stuff
		dataSize = len(self.OutputBuffer)
		print "HTTP/1.x 200 OK"
		print "Content-Type: text/html"
		print "Content-Length: " + str(dataSize) 
		print ""
		print self.OutputBuffer


