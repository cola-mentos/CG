import numpy as np
import random
from vec3 import Vec3
from ray import Ray
from sphere import Sphere  
class Material:
    def scatter(self, ray_in, rec):
        pass

class Lambertian(Material):
    def __init__(self, albedo):
        self.albedo = albedo
    
    def scatter(self, ray_in, rec):
        scatter_dir = rec['normal'] + Vec3.random_in_unit_sphere().unit_vector()
        if scatter_dir.near_zero():
            scatter_dir = rec['normal']
        scattered = Ray(rec['p'], scatter_dir)
        attenuation = self.albedo
        return (True, attenuation, scattered)

class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = min(fuzz, 1.0)
    
    def scatter(self, ray_in, rec):
        reflected = ray_in.dir.unit_vector().reflect(rec['normal'])
        scattered = Ray(rec['p'], reflected + Vec3.random_in_unit_sphere()*self.fuzz)
        attenuation = self.albedo
        return (scattered.dir.dot(rec['normal']) > 0, attenuation, scattered)

class Dielectric(Material):
    def __init__(self, refractive_index):  # 添加构造函数
        self.ri = refractive_index
    
    def scatter(self, ray_in, rec):
        attenuation = Vec3(1.0, 1.0, 1.0)
        etai_over_etat = (1.0 / self.ri) if rec['front_face'] else self.ri
        
        unit_direction = ray_in.dir.unit_vector()
        cos_theta = min((-unit_direction).dot(rec['normal']), 1.0)
        sin_theta = np.sqrt(1.0 - cos_theta**2)
        
        if etai_over_etat * sin_theta > 1.0:
            reflected = unit_direction.reflect(rec['normal'])
            scattered = Ray(rec['p'], reflected)
            return (True, attenuation, scattered)
        
        reflect_prob = self.schlick(cos_theta, etai_over_etat)
        if random.random() < reflect_prob:
            reflected = unit_direction.reflect(rec['normal'])
            scattered = Ray(rec['p'], reflected)
            return (True, attenuation, scattered)
        
        refracted = unit_direction.refract(rec['normal'], etai_over_etat)
        scattered = Ray(rec['p'], refracted)
        return (True, attenuation, scattered)
    
    def schlick(self, cosine, ref_idx):
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0**2
        return r0 + (1 - r0)*pow((1 - cosine),5)