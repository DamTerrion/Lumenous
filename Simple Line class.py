class line (object):
	def __init__ (self, x, y, lenght, width, angle):
		self.x = x
		self.y = y
		self.l = lenght
		self.w = width
		self.a = angle
	
	def pat (size, reverse):
		'''
		if not reverse.type == bool:
			return 'Error:ReverseType'
			break
		if not size in (76, 102, 127, 153):
			return 'Error:WrongSize'
			break
		if self.x > size :
			return 'Error:TooLargeX'
			break
		if self.y > size :
			return 'Error:TooLargeY'
			break
		if self.x < 0 :
			return 'Error:NegativeX'
			break
		if self.y < 0 :
			return 'Error:NegativeY'
			break
		if self.lenght <= 0 :
			return 'Error:ZeroLenght'
			break
		if self.width <= 0 :
			return 'Error:ZeroWidth'
			break
		'''
		if reverse :
			x = round(self.x*1000)
			a = round((self.a % 90)*10)
		else:
			x = size - self.x
			if a :
				a = round(900 - (self.a % 90)*10)
			else :
				a = 0
		y = round(self.y*1000)
		
		if self.a % 180 >= 90 :
			h = round(self.w*1000)
			w = round(self.l*1000)
		else:
			h = round(self.l*1000)
			w = round(self.w*1000)
		
		return {'x':x, 'y':y, 'h':h, 'w':w, 'a':a, 'str':'X'+str(x)+'Y'+str(y)+'H'+str(h)+'W'+str(w)+'A'+str(a)+';\n'}
		
