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
    
    def pat (size, reverse):
        
        if not reverse.type == bool:
            return {'out':'', 'Error':'ReverseType'}
            break
        if not size in (76, 102, 127, 153):
            return {'out':'', 'Error':'Wrong Size'}
            break
        if self.x > size :
            return {'out':'', 'Error':'Too Large X'}
            break
        if self.y > size :
            return {'out':'', 'Error':'Too Large Y'}
            break
        if self.x < 0 :
            return {'out':'', 'Error':'Negative X'}
            break
        if self.y < 0 :
            return {'out':'', 'Error':'Negative Y'}
            break
        if self.lenght <= 0 :
            return {'out':'', 'Error':'Zero Lenght'}
            break
        if self.width <= 0 :
            return {'out':'', 'Error':'ZeroWidth'}
            break
        
        if reverse :
            x = round(self.x)
            a = round(self.a % 900)
        else:
            x = size*1000 - self.x
            if a :
                a = round(- self.a % 900)
            else :
                a = 0
        y = round(self.y)
        
        if self.a % 180 >= 90 :
            h = round(self.w*1000)
            w = round(self.l*1000)
        else:
            h = round(self.l*1000)
            w = round(self.w*1000)
                    
        out = 'X'+str(x)+'Y'+str(y)+'H'+str(h)+'W'+str(w)+'A'+str(a)+';\n'
        return {'x':x, 'y':y, 'h':h, 'w':w, 'a':a, 'out':out, 'Error':False}
    
