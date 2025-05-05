import taichi as ti
import taichi.math as tm
import time
start=time.time()

ti.init(arch=ti.gpu)

n = 320
pixels = ti.Vector.field(3, dtype=ti.f32, shape=(n * 2, n))  

@ti.func
def complex_sqr(z):
    return tm.vec2(z[0] * z[0] - z[1] * z[1], 2 * z[0] * z[1])

@ti.kernel
def paint():
    for i, j in pixels:
        c = tm.vec2(-0.8, 0.156)
        z = tm.vec2(i / n - 1, j / n - 0.5) * 2
        iterations = 0
        while z.norm() < 20 and iterations < 50:
            z = complex_sqr(z) + c
            iterations += 1
    
        if iterations == 50:
            
            pixels[i, j] = tm.vec3(0.0, 0.0, 0.5)  
        else:
            t = iterations / 50.0
            
            r = tm.clamp(0.8 + tm.sin(t * tm.pi * 2) * 0.2, 0.0, 1.0)
            g = tm.clamp(0.4 + tm.sin(t * tm.pi * 1.5) * 0.3, 0.0, 1.0)
            b = tm.clamp(0.6 + tm.sin(t * tm.pi) * 0.2, 0.0, 1.0)
        
            r = tm.pow(r, 0.8)
            g = tm.pow(g, 0.8)
            b = tm.pow(b, 0.8)
        
            pixels[i, j] = tm.vec3(r, g, b)

paint()

gui = ti.GUI("Julia Set", res=(n * 2, n))
gui.set_image(pixels)

gui.show("julia_set.png")  

gui.show()
end=time.time()
print("Running time:%s Seconds"%(end-start))

