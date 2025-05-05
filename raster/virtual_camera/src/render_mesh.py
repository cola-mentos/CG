import numpy as np

from ndc2pixel import ndc2pixel
from save_img import save_array_as_png
from utils import rotate_y_axis
from save_mp4 import save_arrays_as_mp4
import tqdm
from load_obj import load_obj
from draw_triangles import compute_barycentric

if __name__ == "__main__":

    obj_path = "./data/bunny50.obj"

    raw_vertex_array, faces = load_obj(obj_path)
    colors = np.random.rand(faces.shape[0], 3)
    # normalize the vertices
    raw_vertex_array -= raw_vertex_array.mean(axis=0)

    raw_vertex_array /= raw_vertex_array.max()

    raw_vertex_array[:, 2] = raw_vertex_array[:, 2] - 2.0

    # vertex = raw_vertex_array[:, :2]
    # y’ = -f * y/z
    # x’ = -f * x/z
    focal_length = 2.0
    vertex = np.zeros((raw_vertex_array.shape[0], 2), dtype=np.float32)
    vertex[:, 1] = -focal_length * raw_vertex_array[:, 1] / raw_vertex_array[:, 2]
    vertex[:, 0] = -focal_length * raw_vertex_array[:, 0] / raw_vertex_array[:, 2]

    vertex_z = raw_vertex_array[:, 2]

    width, height = 200, 150

    # 转换到像素坐标
    pixel_coords = ndc2pixel(vertex, width, height)

    image = np.zeros((width, height, 3), dtype=np.float32)
    z_buffer = np.zeros((width, height), dtype=np.float32)
    z_buffer.fill(-np.inf)
    for i in tqdm.trange(len(faces)):
        face = faces[i]
        color = colors[i]
        v0_id = int(face[0])
        v1_id = int(face[1])
        v2_id = int(face[2])
        a = pixel_coords[v0_id]
        b = pixel_coords[v1_id]
        c = pixel_coords[v2_id]
        a_z = vertex_z[v0_id]
        b_z = vertex_z[v1_id]
        c_z = vertex_z[v2_id]

        min_x = int(min(a[0], b[0], c[0]))
        max_x = int(max(a[0], b[0], c[0]))
        min_y = int(min(a[1], b[1], c[1]))
        max_y = int(max(a[1], b[1], c[1]))

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if not (x >= 0 and x < width and y >= 0 and y < height):
                    continue

                u, v, w = compute_barycentric(np.array([x, y]), a, b, c)

                z = u * a_z + v * b_z + w * c_z

                if u >= 0 and v >= 0 and w >= 0:
                    if z_buffer[x, y] < z:

                        image[x, y] = color

                        z_buffer[x, y] = z
                        
    depth_img = np.zeros_like(image)
    depth_img[:, :, 0] = -1 / z_buffer
    depth_img[:, :, 1] = -1 / z_buffer
    depth_img[:, :, 2] = -1 / z_buffer

    save_array_as_png(image, "output.png")
    save_array_as_png(depth_img, "depth.png")
