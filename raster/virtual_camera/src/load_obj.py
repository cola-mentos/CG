import trimesh
import numpy as np

def load_obj(obj_path):
    # 使用 trimesh 加载 .obj 文件
    mesh = trimesh.load(obj_path)

    # 提取顶点信息
    vertices = np.array(mesh.vertices)

    # 提取面信息
    faces = np.array(mesh.faces)

    # 提取法线信息
    normals = np.array(mesh.vertex_normals)
   

    return vertices, faces,normals

if __name__ == '__main__':
    obj_path = 'Alien Animal.obj'
   
    vertices, faces, normals = load_obj(obj_path)

    print("Vertices:\n", vertices.shape)
    print("Vertices:\n", vertices.min())
    print("Vertices:\n", vertices.max())
    print("Faces:\n", faces.shape)
    print("Faces:\n", faces.min())
    print("Faces:\n", faces.max())
    print("Normals:\n", normals.shape)
    print("Normals:\n", normals.min())
    print("Normals:\n", normals.max())
    print(normals)
    