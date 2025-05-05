import numpy as np
import tqdm
import taichi as ti 
# 计算三角形abc的面积
@ti.func
def triangle_area(v1, v2, v3):
    return 0.5 * ti.math.cross(v2 - v1, v3 - v1)

@ti.func
def compute_barycentric(p, a, b, c):

    # 计算整个三角形的面积
    A = triangle_area(a, b, c)

    # 计算子三角形的面积
    A_u = triangle_area(p, b, c)
    A_v = triangle_area(a, p, c)
    A_w = triangle_area(a, b, p)

    # 计算重心坐标
    u = A_u / A
    v = A_v / A
    w = A_w / A

    return u, v, w

@ti.kernel
def draw_triangle_ti(image:ti.types.ndarray(), ndc2pixel_coords:ti.types.ndarray(),min_x:int, max_x:int, min_y:int, max_y:int):

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            point_xy = ti.math.vec2(x,y)
            point_0 = ti.math.vec2(ndc2pixel_coords[0,0],ndc2pixel_coords[0,1])
            point_1 = ti.math.vec2(ndc2pixel_coords[1,0],ndc2pixel_coords[1,1])
            point_2 = ti.math.vec2(ndc2pixel_coords[2,0],ndc2pixel_coords[2,1])
            u, v, w = compute_barycentric(
                point_xy,
              point_0,point_1,point_2
            )

            if u >= 0 and v >= 0 and w >= 0:
                image[x, y,0] = 1
                image[x, y,2] = 1

if __name__ == "__main__":
    from save_img import save_array_as_png
    from ndc2pixel import ndc2pixel
    ti.init(arch = ti.cpu)

    # 输入 NDC 坐标，范围为 [-w/h, w/h] x [-1, 1]
    ndc_coords = np.array(
        [
            [0.0, 0.0],
            [-0.5, -0.5],
            [0.5, 0.8],
        ]
    )
    width, height = 1080, 720
    image = np.zeros((width, height, 3), dtype=np.float32)
    ndc2pixel_coords = ndc2pixel(ndc_coords, width, height)
    
    

    min_x = int(ndc2pixel_coords[:, 0].min())
    max_x = int(ndc2pixel_coords[:, 0].max())
    min_y = int(ndc2pixel_coords[:, 1].min())
    max_y = int(ndc2pixel_coords[:, 1].max())
    
    # 30s
    draw_triangle_ti(image, ndc2pixel_coords,min_x, max_x, min_y, max_y)
    
    save_array_as_png(image, "triangle.png")
