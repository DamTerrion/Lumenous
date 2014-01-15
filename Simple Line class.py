class Line(object):
    def __init__ (self, x, y, a, v, width, height):
        self.x = x
        self.y = y
        self.a = a
        self.v = v
        self.angle = a + v*90
        self.width = width
        self.height = height

    def points (self):
        if v % 2 :
            h_length = self.height/2.0
            l_width = self.width
        else:
            h_length = self.width/2.0
            l_width = self.heigth
        x1 = self.x + h_length * cos(pi*self.angle/180)
        y1 = self.y + h_length * sin(pi*self.angle/180)
        x2 = self.x - h_length * cos(pi*self.angle/180)
        y2 = self.y - h_length * sin(pi*self.angle/180)
        return (l_width, {'x': x1, 'y': y1}, {'x': x2, 'y': y2})
