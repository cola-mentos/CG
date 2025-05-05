class Ray:
    def __init__(self, origin, direction):
        self.orig = origin
        self.dir = direction.unit_vector()
    
    def at(self, t):
        return self.orig + self.dir * t