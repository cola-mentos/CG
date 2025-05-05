import numpy as np
import tqdm

# 计算三角形abc的面积
def triangle_area(v1, v2, v3):
    return 0.5 * np.cross(v2 - v1, v3 - v1)

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

def draw_triangle_np(image, ndc2pixel_coords):

    for x in tqdm.trange(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            u, v, w = compute_barycentric(
                np.array([x, y]),
                ndc2pixel_coords[0],
                ndc2pixel_coords[1],
                ndc2pixel_coords[2],
            )

            if u >= 0 and v >= 0 and w >= 0:
                image[x, y] = [1.0, 0.0, 1.0]

if __name__ == "__main__":
    from save_img import save_array_as_png
    from ndc2pixel import ndc2pixel

    # 输入 NDC 坐标，范围为 [-w/h, w/h] x [-1, 1]
    ndc_coords = np.array(
        [
            [0.0, 0.0],
            [-0.5, 0.5],
            [0.5, 0.8],
        ]
    )
    width, height = 300, 200
    image = np.zeros((width, height, 3), dtype=np.float32)
    ndc2pixel_coords = ndc2pixel(ndc_coords, width, height)

    min_x = int(ndc2pixel_coords[:, 0].min())
    max_x = int(ndc2pixel_coords[:, 0].max())
    min_y = int(ndc2pixel_coords[:, 1].min())
    max_y = int(ndc2pixel_coords[:, 1].max())
    
    # 30s
    draw_triangle_np(image, ndc2pixel_coords)
    
    save_array_as_png(image, "triangle.png")
