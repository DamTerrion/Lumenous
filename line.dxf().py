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
                
        return { 'out': out,
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
              'y': self.y + l['y'] - w[1] }
        
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
        
        return { 'out':out,
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
                
        return { 'out':out,
                 '1': p1, '2': p2,
                 '3': p3, '4': p4,
                 'Error':False }
