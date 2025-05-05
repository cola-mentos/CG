import numpy as np
class Sphere:
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    
    def hit(self, ray, t_min, t_max):
        oc = ray.orig - self.center
        a = ray.dir.dot(ray.dir)
        half_b = oc.dot(ray.dir)
        c = oc.dot(oc) - self.radius**2
        discriminant = half_b**2 - a*c
        
        if discriminant > 0:
            root = np.sqrt(discriminant)
            t = (-half_b - root) / a
            if t_min < t < t_max:
                p = ray.at(t)
                normal = (p - self.center) / self.radius
                return (t, p, normal, self.material)
            t = (-half_b + root) / a
            if t_min < t < t_max:
                p = ray.at(t)
                normal = (p - self.center) / self.radius
                return (t, p, normal, self.material)
        return None