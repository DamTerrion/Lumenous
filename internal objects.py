class internal_obj (object):
    points = []
    width = False
    
    def __init__ (self, object_type, layer='0'):
        self.type = object_type
        self.layer = layer
        if object_type = 'POLYLINE':
            self.closed = False

    def add_point (self, number, axis_name, value):
        while len(points) < number :
            points.append({})
        points[number][axis_name] = value

    def count_points (self):
        counter = 0
        for point in self.points :
            if point != {} :
                counter += 1
        return counter
