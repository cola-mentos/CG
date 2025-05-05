import numpy as np


def obj_vertices_to_array(obj_path):
    """
    从OBJ文件中提取顶点数据并转换为numpy数组

    参数:
    obj_path (str): OBJ文件路径

    返回:
    numpy.ndarray: 顶点数组，形状为(M,3)，M为顶点数量
    """
    vertices = []

    with open(obj_path, "r") as f:
        for line in f:
            # 处理以"v "开头的顶点数据行（注意包含空格）
            if line.startswith("v "):
                # 分割数据并转换为浮点数
                parts = line.strip().split()
                vertex = list(map(float, parts[1:4]))  # 取前三个坐标值
                vertices.append(vertex)

    return np.array(vertices)


if __name__ == "__main__":
    from ndc2pixel import ndc2pixel
    from save_img import save_array_as_png
    from utils import rotate_y_axis
    from save_mp4 import save_arrays_as_mp4
    import tqdm
    from load_obj import load_obj

    obj_path = "./data/bunny50.obj"

    raw_vertex_array, faces = load_obj(obj_path)
    # normalize the vertices
    raw_vertex_array -= raw_vertex_array.min(axis=0)

    raw_vertex_array /= raw_vertex_array.max()

    num_frames = 100
    rendering_list = []
    for i in tqdm.trange(num_frames):
        t = i / num_frames
        theta = 360 * t

        vertex_array = rotate_y_axis(raw_vertex_array, theta)

        vertex = vertex_array[:, :2]
        w, h = 720, 480

        # 转换到像素坐标
        pixel_coords = ndc2pixel(vertex, w, h)
        image = np.zeros((w, h, 3), dtype=np.float32)
        for coord in pixel_coords:
            x, y = coord
            if 0 <= x < w and 0 <= y < h:
                image[int(x), int(y), 0] = 1.0

        # save_array_as_png(image, "output.png")
        rendering_list.append(image)

        # print(pixel_coords)
    save_arrays_as_mp4(rendering_list, "output.mp4", fps=30)
