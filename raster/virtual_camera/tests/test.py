import numpy as  np
import tqdm
import taichi as ti 
N = 10000000
# N = 100
a = np.random.randn(N)
b = np.random.randn(N)
c = np.zeros(N)
d = np.zeros(N)

# 20 s


def fun_add(a,b,c):
    for i in tqdm.trange(N):
        c[i] = a[i] + b[i]

@ti.kernel
def fun_add_taichi(a:ti.types.ndarray(),b:ti.types.ndarray(),c:ti.types.ndarray()):
    for i in range(N):
        c[i] = a[i] + b[i]

if __name__ == '__main__':
    import taichi as ti 
    ti.init(arch=ti.cpu)
    fun_add(a,b,c)
    fun_add_taichi(a,b,d)
    print(np.allclose(c,d)) 
    

    
