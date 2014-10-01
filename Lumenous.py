from math import pi, cos, sin, radians
from os.path import exists
from local import say, ask

class Exponion (object):
    def __init__ (self,
                  x, y,
                  height,
                  width,
                  angle,
                  layer='0',
                  origin=None,
                  colour=None
                  ):
        
        self.x  = int(x)
        self.xr = round(self.x)
        
        self.y  = int(y)
        self.yr = round(self.y)
        
        self.h  = int(height)
        self.hr = round(self.h)
        self.hs = str(self.h/1000)
        
        self.w  = int(width)
        self.wr = round(self.w)
        self.ws = str(self.w/1000)
        
        self.a   = int(angle)
        self.ar  = round(self.a)
        self.rad = radians(angle / 10)
        
        self.cos = cos(self.rad)
        self.sin = sin(self.rad)
        
        self.layer  = str(layer)
        self.colour = str(colour)
        self.origin = str(origin)
        
        self.xy = complex (self.x, self.y)
        self.hw = complex (self.w, self.h)
        self.ac = complex (self.cos,
                           self.sin)
    
    def check (self, size=102):
        Correct = 1
        
        Rang = {'76':   30,
                '102':  40,
                '127':  50,
                '153':  60}
        
        if str(size) in Rang:
            Allowed = (int(size)/2 - Rang(str(size)),
                       int(size)/2 + Rang(str(size))
                       )
        else: return {'Correct': 0}
        
        if (abs(self.xr - self.x) > 0.1 or
            abs(self.yr - self.y) > 0.1
            ):
            Correct = 2
        
        if (self.x%0.25 > 0.03 or
            self.y%0.25 > 0.03
            ):
            Correct = 3
        
        if (self.x < Allowed[0] or
            self.x > Allowed[1] or
            self.y < Allowed[0] or
            self.y > Allowed[1]
            ):
            Correct += 4
        
        if (self.x < 0 or self.x > int(size) or
            self.y < 0 or self.y > int(size)
            ):
            Correct += 4
        
        return {'Correct': Correct}
    
    def coords (self):
        va = self.ac * (self.hw.real)
        vb = self.ac * (self.hw - va)
        
        return {'A': self.xy + va,
                'B': self.xy + vb,
                'C': self.xy - va,
                'D': self.xy - vb,
                
                '1': self.xy - va-vb,
                '2': self.xy + va-vb,
                '3': self.xy - va+vb,
                '4': self.xy + va-vb
                }
    
    def pat (self, size=102, reverse=False):
        
        if reverse:
            Check = self.check(size)
        else:
            Check = self.check()
        if not Check['Correct']:
            return {'out': '', 'Error': Check['Error']}
        
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
            w = self.hr
        else:
            h = self.hr
            w = self.wr
        
        return {'x': x, 'y': y, 'h': h, 'w': w, 'a': a,
                'out': ''.join(('X', str(x),
                                'Y', str(y),
                                'H', str(h),
                                'W', str(w),
                                'A', str(a), ';\n'
                                ))
                }
    
    def polyline (self):
        coord = self.coords()
        result = ['  0', 'POLYLINE',
                  '  8', self.layer]
        if self.colour:
            result += [' 62', '{:>6}'.format(self.colour)]
        result += [' 66', '     1',
                   ' 40', self.ws,
                   ' 41', self.ws]
        result += vertex(coord['C'])
        result += vertex(coord['A'])
        result += ['  0', 'SEQEND',
                   '  8', self.layer]
        return result
    
    def rectangle (self):
        coord = self.coords()
        result = ['  0', 'POLYLINE',
                  '  8', self.layer]
        if self.colour:
            result += [' 62', '{:>6}'.format(self.colour)]
        result += [' 66', '     1',
                   ' 40', '0.0',
                   ' 41', '0.0',
                   ' 70', '     1']
        result += vertex(coord['1'])
        result += vertex(coord['2'])
        result += vertex(coord['4'])
        result += vertex(coord['3'])
        result += ['  0', 'SEQEND'+
                   '  8', self.layer]
        return result
    
    def solid (self):
        coord = self.coords()
        result = ['  0', 'SOLID',
                  '  8', self.layer]
        if self.colour:
            result += [' 62', '{:>6}'.format(self.colour)]
        result += vertex(coord['1'], False)
        result += vertex(coord['2'], False)
        result += vertex(coord['3'], False)
        result += vertex(coord['4'], False)
        return result

class Poynting (list):
    def __init__ (self, stack=None, data_type=None):
        if (data_type.lower() == 'dxf' and
            isinstance(stack, list)):
            pass
        
        if (data_type.lower() == 'pat' and
            isinstance(stack, list)):
            pass
        
        if (data_type.lower() == 'lum' and
            isinstance(stack, list)):
            pass
    
    def add (self, addition):
        if isinstance(addition, Exponion):
            self.append(addition)
        elif isinstance(addition, Poynting) or
             isinstance(addition, list):
            self.extend(addition)
    
    def extend (self, stack):
        for item in stack:
            if isinstance(item, Exponion):
                self.append(item)
    
    def generate (self, form='lum', mode=None):
        if not (isinstance(form, str) and
                form.lower() in ('pat', 'dxf', 'lum')
                ):
            return False
        
        result = []
        if form == 'pat':
            for item in self:
                result += item.pat(mode[0], mode[1])
            result.append('$;')
        
        if form == 'dxf':
            result += ['  0', 'SECTION',
                       '  2', 'ENTITIES']
            for item in self:
                if mode == 'polyline':
                    result += self.polyline()
                elif mode == 'solid':
                    result += self.solid()
                elif mode == 'rectangle':
                    result += self.rectangle()
                elif self.orig == 'SOLID':
                    result += self.solid()
                else:
                    result += self.polyline()
            result += ['  0', 'ENDSEC',
                       '  0', 'EOF']

        if form == 'lum':
            pass

        return '\n'.join(result)
        
    def layer (self, name=False):
        if name:
            result = Poynting()
            for item in self:
                if item.layer == name: result.add(item)
            return result

        result = dict()
        for item in self:
            if not item.layer in result:
                result[item.layer] = Poynting()
            result[item.layer].add(item)
        return result
    
    def data_file (self, name='data'):
        result = [name, ' = {\n']
        space = ' '*4
        for item in self:
            result += [space,
                       'Exponion(',
                       str(self.x), ', ',
                       str(self.y), ', ',
                       str(self.h), ', ',
                       str(self.w), ', ',
                       str(self.a), ', ',
                       self.layer,  ', ',
                       self.origin, ', ',
                       self.colour, ')\n']
        result += [space, '}\n']
        return ''.join(result)
    
    def check (self, size):
        for item in self:
            pass

def vertex (point, full=True):
    if not isinstance(point, complex): return False
    result = []
    if full:
        result += ['  0', 'VERTEX',
                   '  8', self.layer]
    result += [' 10', str(point.real/1000),
              [' 20', str(point.imag/1000)]
    if full:
        result += [' 30', '0.0']
    return result
