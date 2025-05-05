import numpy as np
import random

class Vec3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.e = np.array([x, y, z], dtype=np.float64)
    
    @property
    def x(self): return self.e[0]
    @property
    def y(self): return self.e[1]
    @property
    def z(self): return self.e[2]
    
    def __add__(self, other): return Vec3(*(self.e + other.e))
    def __sub__(self, other): return Vec3(*(self.e - other.e))
    def __mul__(self, other):
        if isinstance(other, Vec3): return Vec3(*(self.e * other.e))
        return Vec3(*(self.e * other))
    def __truediv__(self, t): return Vec3(*(self.e / t))
    
    def dot(self, v): return np.dot(self.e, v.e)
    def cross(self, v): return Vec3(*np.cross(self.e, v.e))
    def length(self): return np.linalg.norm(self.e)
    def unit_vector(self): return self / self.length()
    def near_zero(self):
        # 判断向量是否接近零（各分量绝对值小于1e-8）
        s = 1e-8
        return (abs(self.x) < s) and (abs(self.y) < s) and (abs(self.z) < s)
    def reflect(self, n):
        # 计算入射方向v关于法线n的反射方向
        return self - n * self.dot(n) * 2.0
    def refract(self, n, etai_over_etat):
        cos_theta = min((-self).dot(n), 1.0)
        r_out_perp = (self + n * cos_theta) * etai_over_etat
        r_out_parallel = n * -np.sqrt(abs(1.0 - r_out_perp.length()**2))
        return r_out_perp + r_out_parallel
    @staticmethod
    def random(min=0.0, max=1.0):
        return Vec3(random.uniform(min, max),
                    random.uniform(min, max),
                    random.uniform(min, max))
    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)  # 显式创建新向量
    def __mul__(self, other):
        if isinstance(other, Vec3):
            return Vec3(self.x*other.x, self.y*other.y, self.z*other.z)
        return Vec3(self.x*other, self.y*other, self.z*other)
    def __rmul__(self, other):
        return self.__mul__(other)
    @staticmethod
    def random_in_unit_sphere():
        while True:
            p = Vec3.random(-1, 1)
            if p.length() < 1:
                return p