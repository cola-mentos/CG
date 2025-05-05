import numpy as np
from ndc2pixel import ndc2pixel
from save_img import save_array_as_png
import tqdm
import taichi as ti 

@ti.kernel
def draw_circle_kernel_ti(height:int,width:int,center_pixel:ti.types.ndarray(),radius:float,img:ti.types.ndarray()):
    for y in range(height):
        for x in range(width):
            center_pixel_point = ti.math.vec2(center_pixel[0,0],center_pixel[0,1])
            xy_point = ti.math.vec2(x,y)
            
            if (xy_point-center_pixel_point).norm() <= radius:
                img[x, y, 0 ] = 1
                img[x, y, 2 ] = 1
            
                

def draw_circle_kernel_np(height,width,center_pixel,radius,img):
    for y in tqdm.trange(height):
        for x in range(width):
            
            if np.linalg.norm([x, y] - center_pixel[0]) <= radius:
                img[x, y] = [1.0, 0.0, 1.0]

def draw_circle(backend='np'):
    center = np.array([[0.3, -.2]])
    width, height = 1080, 720
    radius = 0.5 * height/2
    center_pixel = ndc2pixel(center, width, height)
    print(center_pixel.shape)
    

    img = np.zeros((width, height, 3), dtype=np.float32)
    
    if backend == 'np':
        draw_circle_kernel = draw_circle_kernel_np
    elif backend == 'ti':
        draw_circle_kernel = draw_circle_kernel_ti
    else:
        raise ValueError(f'Unknown backend: {backend}')
    
    draw_circle_kernel(height,width,center_pixel,radius,img)
    
    save_array_as_png(img,'circle.png')
    


if __name__ == "__main__":
    ti.init(arch=ti.cpu)
    draw_circle('ti')
    
