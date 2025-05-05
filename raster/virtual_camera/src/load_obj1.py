import trimesh
import numpy as np

def load_obj(obj_path):
    # 加载 OBJ 文件，并确保返回的是 Mesh 对象
    mesh_data = trimesh.load(obj_path)
    
    # 情况 1：如果加载的是 Scene 对象（包含多个网格）
    if isinstance(mesh_data, trimesh.Scene):
        # 合并场景中的所有网格，或选择第一个网格（根据需求调整）
        mesh = mesh_data.to_geometry()
    # 情况 2：如果加载的是单个 Mesh 对象
    elif isinstance(mesh_data, trimesh.Trimesh):
        mesh = mesh_data
    else:
        raise ValueError("Unsupported data type: {}".format(type(mesh_data)))
    
    # 提取顶点信息
    vertices = np.array(mesh.vertices)
    
    # 提取面信息
    faces = np.array(mesh.faces)
    
    # 提取法线信息（如果不存在则生成）
    if hasattr(mesh, 'vertex_normals') and mesh.vertex_normals is not None:
        normals = np.array(mesh.vertex_normals)
    else:
        # 若法线不存在，尝试生成（trimesh 会自动计算）
        mesh.vertex_normals = mesh.vertex_normals
        normals = np.array(mesh.vertex_normals)
    
    return vertices, faces, normals

if __name__ == '__main__':
    obj_path = 'Wolf_One_obj.obj'
    try:
        vertices, faces, normals = load_obj(obj_path)
        print("Vertices shape:", vertices.shape)
        print("Vertices min/max:", vertices.min(), vertices.max())
        print("Faces shape:", faces.shape)
        print("Faces min/max:", faces.min(), faces.max())
        print("Normals shape:", normals.shape)
        print("Normals min/max:", normals.min(), normals.max())
    except Exception as e:
        print("Error:", str(e))