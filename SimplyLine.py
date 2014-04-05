from math import pi, cos, sin

class Line (object):
    def __init__ (self, x, y, lenght, width, angle, layer):
        self.x = x
        self.xr = round(x)
        
        self.y = y
        self.yr = round(y)
        
        self.l = lenght
        self.lr = round(lenght)
        self.ls = str(lenght/1000)
        
        self.w = width
        self.wr = round(width)
        self.ws = str(width/1000)
        
        self.a = angle
        self.ar = round(angle)
        self.rad = (angle * pi / 1800) % (2 * pi)
        
        self.layer = str(layer)
        self.cos = cos(self.rad)
        self.sin = sin(self.rad)

        self.xy = complex (self.x, self.y)
        self.lw = complex (self.l, self.w)
        self.ac = complex (self.cos,
                           self.sin)

    def check (self, size=False):
        Correct, Errors = True, []
        
        if size :
            if self.x >= size : Errors.append('Too Large X')
            if self.y >= size : Errors.append('Too Large Y')
        if self.x <= 0 : Errors.append('Negative X')
        if self.y <= 0 : Errors.append('Negative Y')
        if self.l <= 0 : Errors.append('Zero Lenght')
        if self.w <= 0 : Errors.append('Zero Width')

        if len(Errors): Correct = False
        return {'Correct': Correct, 'Error': Errors }

    def coords (self):
        A = self.lw.real
        B = self.lw - A

    def pat (self, size, reverse):

        Plate = plate(size)
        if not type(Plate) is tuple:
            return {'out': '', 'Error': Plate }
        if not type(reverse) is bool:
            return {'out': '', 'Error': 'Wrong Reverse Type'}
        
        if reverse:
            Check = self.check(Plate[1])
        else:
            Check = self.check()
        if not Check['Correct']:
            return {'out': '', 'Error': Check['Error'] }
        
        if reverse :
            x = self.xr
            a = self.ar % 900
        else:
            x = size*1000 - self.xr
            if a :
                a = 900 - (self.ar % 900)
            else :
                a = 0
        y = self.yr
        
        if self.a % 1800 >= 900 :
            h = self.wr
            w = self.lr
        else:
            h = self.lr
            w = self.wr
        
        return {'x': x, 'y': y, 'h': h, 'w': w, 'a': a,
                'out': ('X'+str(x)+
                        'Y'+str(y)+
                        'H'+str(h)+
                        'W'+str(w)+
                        'A'+str(a)+';\n') }
        
    def polyline (self):
        l = { 'x': self.l * self.cos,
              'y': self.l * self.sin }
              
        p1 = {'x': self.x - l['x'],
              'y': self.y - l['y'] }
              
        p2 = {'x': self.x + l['x'],
              'y': self.y + l['y'] }
              
        out = ( '  0\nPOLYLINE\n'+
                '  8\n'+self.layer+'\n'+
                ' 66\n1\n'+
                ' 40\n'+self.ws+'\n'+
                ' 41\n'+self.ws+'\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p1['x']/1000)+'\n'+
                ' 20\n'+str(p1['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p2['x']/1000)+'\n'+
                ' 20\n'+str(p2['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nSEQEND\n'+
                '  8\n'+self.layer+'\n' )
                
        return {'out': out,
                '1': p1, '2': p2,
                'Error': False }
        
    def rectangle (self):
        l = { 'x': self.l * self.cos,
              'y': self.l * self.sin }
        
        w = { 'x': self.w * self.sin,
              'y': self.w * self.cos }
        
        p1 = {'x': self.x - l['x'] + w['x'],
              'y': self.y - l['y'] + w['y'] }
        
        p2 = {'x': self.x + l['x'] + w['x'],
              'y': self.y + l['y'] + w['y'] }
        
        p3 = {'x': self.x + l['x'] - w['x'],
              'y': self.y + l['y'] - w['y'] }
        
        p4 = {'x': self.x - l['x'] - w['x'],
              'y': self.y - l['y'] - w['y'] }
        
        out = ( '  0\nPOLYLINE\n'+
                '  8\n'+self.layer+'\n'+
                ' 66\n1\n'+
                ' 40\n0.0\n'+
                ' 41\n0.0\n'+
                ' 70\n1\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p1['x']/1000)+'\n'+
                ' 20\n'+str(p1['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p2['x']/1000)+'\n'+
                ' 20\n'+str(p2['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p3['x']/1000)+'\n'+
                ' 20\n'+str(p3['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nVERTEX\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p4['x']/1000)+'\n'+
                ' 20\n'+str(p4['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                '  0\nSEQEND\n'+
                '  8\n'+self.layer+'\n' )
        
        return {'out':out,
                '1': p1, '2': p2,
                '3': p3, '4': p4,
                'Error': False }
        
    def solid (self):
        coord = self.rectangle()
        p1 = coord['1']
        p2 = coord['2']
        p3 = coord['4']
        p4 = coord['3']
        
        out = ( '  0\nSOLID\n'+
                '  8\n'+self.layer+'\n'+
                ' 10\n'+str(p1['x']/1000)+'\n'+
                ' 20\n'+str(p1['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                ' 11\n'+str(p2['x']/1000)+'\n'+
                ' 21\n'+str(p2['y']/1000)+'\n'+
                ' 31\n0.0\n'+
                ' 12\n'+str(p3['x']/1000)+'\n'+
                ' 22\n'+str(p3['y']/1000)+'\n'+
                ' 32\n0.0\n'+
                ' 13\n'+str(p4['x']/1000)+'\n'+
                ' 23\n'+str(p4['y']/1000)+'\n'+
                ' 33\n0.0\n' )
                
        return {'out':out,
                '1': p1, '2': p2,
                '3': p3, '4': p4,
                'Error': False }
