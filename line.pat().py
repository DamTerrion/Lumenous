from math import pi
from math import cos
from math import sin

class Line (object):
    def __init__ (self, x, y, lenght, width, angle, layer):
        self.x = x
        self.rx = round(x)
        self.y = y
        self.ry = round(y)
        self.l = lenght
        self.ls = str(lenght/1000)
        self.w = width
        self.ws = str(width/1000)
        self.a = angle
        self.rad = (angle * pi / 1800) % (2 * pi)
        self.layer = layer
        self.cos = cos(self.rad)
        self.sin = sin(self.rad)
    
    def pat (plate, reverse):
        # Параметр "plate" обозначает тип пластины в формате A102x4 или M127
        # Первая литера обозначает: A - лазерный генератор, M - эмульсионный
        # Параметр "reverse" обозначает необходимость переворота изображения
        # Reverse True - стандартный вид (со стороны стекла)
        # Reverse False - неперевёрнутый со стороны покрытия (для контактной печати, промежуточных ФШ, прямого использования, сеткографии)

        gen = False
        if type(plate) == str :
            if plate[0] in ('A', 'M'):
                gen = plate[0]
                plate = plate[1:]
            
            if plate[0] in '1234567890':
                size = ''
                while not plate[0] in '1234567890':
                    size += plate[0]
                    plate = plate[1:]
                size = int(size)
            elif reverse :
                return { 'out':'', 'Error':'Reverse with has No Plate Size' }
                break
            else:
                size = 0
            
            if plate[0:2] == 'x4'
                mash = 4
            else:
                mash = 1
            if size and not size in (76, 102, 127, 153):
                return { 'out':'', 'Error':'Wrong Plate Size' }
                break
        
        if not type(reverse) == bool:
            return { 'out':'', 'Error':'Wrong Reverse Type' }
            break
        if size and self.x > size :
            return {'out':'', 'Error':'Too Large X'}
            break
        if size and self.y > size :
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
            return {'out':'', 'Error':'Zero Width'}
            break
        
        if reverse :
            x = self.rx
            a = round(self.a % 900)
        else:
            x = size*1000 - self.rx
            if a :
                a = 900 - round(self.a % 900)
            else :
                a = 0
        y = self.ry
        
        if self.a % 1800 >= 900 :
            h = round(self.w)
            w = round(self.l)
        else:
            h = round(self.l)
            w = round(self.w)
        
        return {'x':x, 'y':y, 'h':h, 'w':w, 'a':a, 'out':'X'+str(x)+'Y'+str(y)+'H'+str(h)+'W'+str(w)+'A'+str(a)+';\n'}
        
