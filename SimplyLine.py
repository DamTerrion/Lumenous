from math import pi, cos, sin, radians

class Line (object):
    def __init__ (self, x, y, lenght, width, angle,
                  layer='0', origin=None, colour=None):
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
        self.rad = radians(angle / 10)
        
        self.cos = cos(self.rad)
        self.sin = sin(self.rad)
        
        self.layer  = str(layer)
        self.colour = str(colour)
        self.origin = str(origin)
        
        self.xy = complex (self.x, self.y)
        self.lw = complex (self.w, self.l)
        self.ac = complex (self.cos,
                           self.sin)
    
    def check (self, size=102):
        Correct_code = 1
        
        if size == 102:
            Rang1 = (0, 102)
            Rang2 = (51-40, 51+40)
        if size == 127:
            Rang1 = (0, 127)
            Rang2 = (63.5-50, 63.5+50)
        
        if (self.x%1 > 0.1 or self.y%1 > 0.1):
            Correct_code = 2
        if (self.x%0.25 > 0.1 or self.y%0.25 > 0.1):
            Correct_code = 3
        
        return { 'Correct': Correct }
    
    def coords (self):
        va = self.ac * ( self.lw.real )
        vb = self.ac * ( self.lw - va )
        
        return {'A': self.xy + va,
                'B': self.xy + vb,
                'C': self.xy - va,
                'D': self.xy - vb,
                
                '1': self.xy - va - vb,
                '2': self.xy + va - vb,
                '3': self.xy - va + vb,
                '4': self.xy + va - vb
                }

    def colour_string (self):
        if self.colour:
            return ' 62\n{:>6}\n'.format(self.colour)
        return ''
    
    def pat (self, size=102, reverse=False):
        
        if reverse:
            Check = self.check(size)
        else:
            Check = self.check()
        if not Check['Correct']:
            return {'out': '', 'Error': Check['Error'] }
        
        if reverse :
            x = self.xr
            a = self.ar % 900
        else:
            x = size*1000 - self.xr
            if self.a :
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
        coord = self.coords()
        
        A = {'x': coord['A'].real,
             'y': coord['A'].imag }
        
        C = {'x': coord['C'].real,
             'y': coord['C'].imag }
        
        return (' 0\nPOLYLINE\n'+
                ' 8\n'+self.layer+'\n'+
                colour_string()+
                ' 66\n     1\n'+
                ' 40\n'+self.ws+'\n'+
                ' 41\n'+self.ws+'\n'+
                ' 0\nVERTEX\n'+
                ' 8\n'+self.layer+'\n'+
                ' 10\n'+str(C['x']/1000)+'\n'+
                ' 20\n'+str(C['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                ' 0\nVERTEX\n'+
                ' 8\n'+self.layer+'\n'+
                ' 10\n'+str(A['x']/1000)+'\n'+
                ' 20\n'+str(A['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                ' 0\nSEQEND\n'+
                ' 8\n'+self.layer+'\n' )
    
    def rectangle (self):
        coord = self.coords()
        
        p1 = {'x': coord['1'].real,
              'y': coord['1'].imag }
        
        p2 = {'x': coord['2'].real,
              'y': coord['2'].imag }
        
        p3 = {'x': coord['4'].real,
              'y': coord['4'].imag }
        
        p4 = {'x': coord['3'].real,
              'y': coord['3'].imag }
        
        return ('  0\nPOLYLINE\n'+
                '  8\n'+self.layer+'\n'+
                colour_string()+
                ' 66\n     1\n'+
                ' 40\n0.0\n'+
                ' 41\n0.0\n'+
                ' 70\n1\n'+
                ' 0\nVERTEX\n'+
                ' 8\n'+self.layer+'\n'+
                ' 10\n'+str(p1['x']/1000)+'\n'+
                ' 20\n'+str(p1['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                ' 0\nVERTEX\n'+
                ' 8\n'+self.layer+'\n'+
                ' 10\n'+str(p2['x']/1000)+'\n'+
                ' 20\n'+str(p2['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                ' 0\nVERTEX\n'+
                ' 8\n'+self.layer+'\n'+
                ' 10\n'+str(p3['x']/1000)+'\n'+
                ' 20\n'+str(p3['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                ' 0\nVERTEX\n'+
                ' 8\n'+self.layer+'\n'+
                ' 10\n'+str(p4['x']/1000)+'\n'+
                ' 20\n'+str(p4['y']/1000)+'\n'+
                ' 30\n0.0\n'+
                ' 0\nSEQEND\n'+
                ' 8\n'+self.layer+'\n' )
    
    def solid (self):
        coord = self.coords()
        
        p1 = {'x': coord['1'].real,
              'y': coord['1'].imag }
        
        p2 = {'x': coord['2'].real,
              'y': coord['2'].imag }
        
        p3 = {'x': coord['3'].real,
              'y': coord['3'].imag }
        
        p4 = {'x': coord['4'].real,
              'y': coord['4'].imag }

        return ('  0\nSOLID\n'+
                '  8\n'+self.layer+'\n'+
                colour_string()+
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

class LStack (list):
    def __init__ (self, stack=None, data_type=None):
        if (data_type.lower() == 'dxf' and
            type(stack) == list:
            pass
        if (data_type.lower() == 'pat' and
            type(stack) == list:
            pass
    
    def add (self, addition):
        if type(addition) == Line:
            self.append(addition)
        elif ( type(addition) == LStack or
               type(addition) == list ):
            self.extend(addition)
    
    def extend (self, stack):
        for item in stack:
            if type(item) == Line:
                self.append(item)
    
    def generate (self, form, mode):
        if not form in ('pat', 'dxf'): return False
        
        result = ''
        if form == 'pat':
            for item in self:
                result += item.pat(mode[0], mode[1])
            result += '$;'
            return result
        
        if form == 'dxf':
            result += ('  0\nSECTION\n'+
                       '  2\nENTITIES\n')
            for item in self:
                if mode == 'polyline':
                    result += self.polyline()
                elif mode == 'solid':
                    result += self.solid()
                elif mode == 'rectangle':
                    result += self.rectangle()
                elif self.orig == 'SOLID':
                    result += self.solid()
                else: result += self.polyline()
            result += ('  0\nENDSEC\n'+
                       '  0\nEOF\n')
            return result
        
    def layer (self, name=False):
        if name:
            result = LStack()
            for item in self:
                if item.layer == name: result.add(item)
            return result

        result = dict()
        for item in self:
            if not item.layer in self:
                result[item.layer] = LStack()
            result[item.layer].add(item)
        return result
    
    def data_file (self, name=data):
        result = name+' = {\n'
        space = ' '*4
        for item in self:
            result += (space + 'Line( '+
                       str(self.x)+', '+
                       str(self.y)+', '+
                       str(self.l)+', '+
                       str(self.w)+', '+
                       str(self.a)+', '+
                       self.layer +', '+
                       self.origin+', '+
                       self.colour+')\n')
        result += space + '}\n'
        return result
    
    def check (self, size):
        for item in self:
            
