class line (object):
	def __init__ (self, x, y, lenght, width, angle, layer):
		self.x = x
		self.y = y
		self.l = lenght
		self.w = width
		self.ws = str(width)
		self.a = angle
		self.rad = (angle * pi() / 1800) % (2 * pi())
		self.layer = layer

	def dxf (self, method):
		if method == 'line' :
			l = ( self.l * cos(self.rad), self.l * sin(self.rad) )
			p1 = ( self.x + l[0], self.y + l[1] ) 
			p2 = ( self.x - l[0], self.y - l[1] )
			out = '  0\nPOLYLINE\n'+
'  8\n'+self.layer+'\n'+
' 40\n'+self.ws+'\n'+
' 41\n'+self.ws+'\n'+
'  0\nVERTEX\n'+
'  8\n'+self.layer+'\n'+
' 10\n'+str(p1[0])+'\n'+
' 20\n'+str(p1[1])+'\n'+
' 30\n0.0\n'+
'  0\nVERTEX\n'+
'  8\n'+self.layer+'\n'+
' 10\n'+str(p2[0])+'\n'+
' 20\n'+str(p2[1])+'\n'+
' 30\n0.0\n'+
'  0\nSEQEND\n'+
'  8\n'+self.layer+'\n'
			return {'out':out, '1':{'x':x1, 'y':y1}, '2':{'x':x2, 'y':y2}, 'Error':False}
		
		elif method == 'rect' :
			c = cos(self.rad)
			s = sin(self.rad)
			l = ( self.l * c, self.l * s )
			w = ( self.w * s, self.w * c) 
			p1 = ( self.x + l[0] + w[0], self.y + l[1] + w[1] )
			p2 = ( self.x + l[0] - w[0], self.y + l[1] - w[1] )
			p3 = ( self.x - l[0] - w[0], self.y - l[1] - w[1] )
			p4 = ( self.x - l[0] + w[0], self.y - l[1] + w[1] )
		
		elif method == 'solid' :
			c = cos(self.rad)
			s = sin(self.rad)
			l = ( self.l * c, self.l * s )
			w = ( self.w * s, self.w * c) 
			p1 = ( self.x + l[0] + w[0], self.y + l[1] + w[1] )
			p2 = ( self.x + l[0] - w[0], self.y + l[1] - w[1] )
			p3 = ( self.x - l[0] + w[0], self.y - l[1] + w[1] )
			p4 = ( self.x - l[0] - w[0], self.y - l[1] - w[1] )

		else:
			return {'out':'', 'Error':'Wrong Method'}
