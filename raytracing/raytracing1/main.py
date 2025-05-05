from PIL import Image
import numpy as np
from vec3 import Vec3
from ray import Ray
from sphere import Sphere
from camera import Camera
from material import Lambertian, Metal, Dielectric
import random
import tqdm
def ray_color(ray, world, depth=50):
    if depth <= 0:
        return Vec3(0,0,0)
    
    hit_record = None
    closest_so_far = np.inf
    for obj in world:
        rec = obj.hit(ray, 0.001, closest_so_far)
        if rec:
            hit_record = {
                't': rec[0],
                'p': rec[1],
                'normal': rec[2],
                'material': rec[3],
                'front_face': (ray.dir.dot(rec[2]) < 0)
            }
            closest_so_far = rec[0]
    
    if hit_record:
        result = hit_record['material'].scatter(ray, hit_record)
        if result[0]:
            return result[1] * ray_color(result[2], world, depth-1)
        return Vec3(0,0,0)
    
    unit_direction = ray.dir.unit_vector()
    t = 0.5*(unit_direction.y + 1.0)
    return Vec3(1.0,1.0,1.0)*(1.0-t) + Vec3(0.5,0.7,1.0)*t

def main():
    aspect_ratio = 16/9
    width = 320
    height = int(width / aspect_ratio)
    samples = 25
    max_depth = 20

    world = []

    world.append(Sphere(Vec3(0, -1000, 0), 1000, Lambertian(Vec3(0.5, 0.5, 0.5))))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.random()
            center = Vec3(a + 0.9*random.random(), 0.2, b + 0.9*random.random())
            
            if (center - Vec3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    albedo = Vec3.random(0.0, 1.0) * Vec3.random(0.0, 1.0)
                    world.append(Sphere(center, 0.2, Lambertian(albedo)))
                elif choose_mat < 0.95:
                    albedo = Vec3.random(0.5, 1.0)
                    fuzz = random.uniform(0, 0.5)
                    world.append(Sphere(center, 0.2, Metal(albedo, fuzz)))
                else:
                    world.append(Sphere(center, 0.2, Dielectric(1.5)))

    world.append(Sphere(Vec3(0, 1, 0), 1.0, Dielectric(1.5)))          # 玻璃球
    world.append(Sphere(Vec3(-4, 1, 0), 1.0, Lambertian(Vec3(0.4, 0.2, 0.1)))) # 漫反射球
    world.append(Sphere(Vec3(4, 1, 0), 1.0, Metal(Vec3(0.7, 0.6, 0.5), 0.0)))  # 金属球

    lookfrom = Vec3(13, 2, 3)
    lookat = Vec3(0, 0, 0)
    vup = Vec3(0, 1, 0)
    cam = Camera(lookfrom, lookat, vup, 20, aspect_ratio, 0.1, 10)
    
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    
    for j in tqdm.trange(height):
        for i in range(width):
            pixel_color = Vec3(0,0,0)
            for _ in range(samples):
                u = (i + random.random()) / (width-1)
                v = 1.0 - (j + random.random()) / (height-1)
                ray = cam.get_ray(u, v)
                pixel_color += ray_color(ray, world, max_depth)
            
            scale = 1.0 / samples
            r = np.sqrt(pixel_color.x * scale)
            g = np.sqrt(pixel_color.y * scale)
            b = np.sqrt(pixel_color.z * scale)
            
            pixels[i,j] = (
                int(255 * np.clip(r, 0, 0.999)),
                int(255 * np.clip(g, 0, 0.999)),
                int(255 * np.clip(b, 0, 0.999))
            )
    
    img.save("final.png")
    img.show()

if __name__ == "__main__":
    main()