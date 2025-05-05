import numpy as np
import math as m
from src.ndc2pixel import ndc2pixel
from utils.save_img import save_array_as_png
from utils.utils import rotate_y_axis
from utils.save_mp4 import save_arrays_as_mp4
import tqdm
from src.load_obj1 import load_obj
from src.draw_triangles_ti import compute_barycentric
import taichi as ti
import os

@ti.kernel
def render_faces(faces:ti.types.ndarray(),pixel_coords:ti.types.ndarray(),vertex_x:ti.types.ndarray(),vertex_y:ti.types.ndarray(),vertex_z:ti.types.ndarray(),colors:ti.types.ndarray(),z_buffer:ti.types.ndarray(),image:ti.types.ndarray(),width:int,height:int,vertex_normals:ti.types.ndarray(),light_pos:ti.types.ndarray()):
    for i in range(faces.shape[0]):
        face = ti.math.vec3(faces[i,0],faces[i,1],faces[i,2])
        light_pos_ti = ti.math.vec3(light_pos[0],light_pos[1],light_pos[2])
        
        v0_id = int(face[0])
        v1_id = int(face[1])
        v2_id = int(face[2])
        n0 = ti.math.vec3(vertex_normals[v0_id,0],vertex_normals[v0_id,1],vertex_normals[v0_id,2])
        n1 = ti.math.vec3(vertex_normals[v1_id,0],vertex_normals[v1_id,1],vertex_normals[v1_id,2])
        n2 = ti.math.vec3(vertex_normals[v2_id,0],vertex_normals[v2_id,1],vertex_normals[v2_id,2])
        a = ti.math.vec2(pixel_coords[v0_id,0],pixel_coords[v0_id,1])
        b = ti.math.vec2(pixel_coords[v1_id,0],pixel_coords[v1_id,1])
        c = ti.math.vec2(pixel_coords[v2_id,0],pixel_coords[v2_id,1])
        
        a_x = vertex_x[v0_id]
        b_x = vertex_x[v1_id]
        c_x = vertex_x[v2_id]

        a_y = vertex_y[v0_id]
        b_y = vertex_y[v1_id]
        c_y = vertex_y[v2_id]

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
                point_xy = ti.math.vec2(x,y)
                u, v, w = compute_barycentric(point_xy, a, b, c)

                z = u * a_z + v * b_z + w * c_z

                if u >= 0 and v >= 0 and w >= 0:
                    if z_buffer[x, y] < z:
                        # max(0,dot(n,l))
                        n = u * n0 + v * n1 + w * n2
                        tmp_x = u * a_x + v * b_x + w * c_x
                        tmp_y = u * a_y + v * b_y + w * c_y
                        l = light_pos_ti - ti.math.vec3(tmp_x, tmp_y, z)
                        n = ti.math.normalize(n)
                        l = ti.math.normalize(l)
                        intensity = max(0, ti.math.dot(n, l))

                        image[x, y,0] = 1 * intensity
                        image[x, y,1] = 1 * intensity
                        image[x, y,2] = 0 * intensity

                        z_buffer[x, y] = z
def render_mesh(raw_vertex_array, faces, vertex_normals,light_pos):
    
    width, height = 720 , 480

    # vertex = raw_vertex_array[:, :2]
    # y’ = -f * y/z
    # x’ = -f * x/z
    focal_length = 2.0
    vertex = np.zeros((raw_vertex_array.shape[0], 2), dtype=np.float32)
    vertex[:, 1] = -focal_length * raw_vertex_array[:, 1] / raw_vertex_array[:, 2]
    vertex[:, 0] = -focal_length * raw_vertex_array[:, 0] / raw_vertex_array[:, 2]
    vertex_x = raw_vertex_array[:, 0]
    vertex_y = raw_vertex_array[:, 1]
    vertex_z = raw_vertex_array[:, 2]
    
    vertex_x = np.ascontiguousarray(vertex_x,dtype=np.float32)
    vertex_y = np.ascontiguousarray(vertex_y,dtype=np.float32)
    vertex_z = np.ascontiguousarray(vertex_z,dtype=np.float32)
    
    

    # 转换到像素坐标
    pixel_coords = ndc2pixel(vertex, width, height)


    image = np.zeros((width, height, 3), dtype=np.float32)
    z_buffer = np.zeros((width, height), dtype=np.float32)
    z_buffer.fill(-np.inf)
    render_faces(faces,pixel_coords,vertex_x,vertex_y,vertex_z,colors,z_buffer,image,width,height,vertex_normals,light_pos)
    
                        
    depth_img = np.zeros_like(image)
    depth_img[:, :, 0] = -1 / z_buffer
    depth_img[:, :, 1] = -1 / z_buffer
    depth_img[:, :, 2] = -1 / z_buffer

    return image

if __name__ == "__main__":
    from utils.utils import rotate_y_axis
    from src.camera import Camera
    from icecream import ic
    ti.init(arch = ti.cpu)

    #obj_path = "armadillo.obj"
    #obj_path = "truck.obj"
    obj_path = "bunny70k_f.obj"

    raw_vertex_array, faces, vertex_normals = load_obj(obj_path)
    colors = np.random.rand(faces.shape[0], 3)
    raw_vertex_array -= raw_vertex_array.mean(axis=0)

    raw_vertex_array /= raw_vertex_array.max()
    
    camera = Camera()

    raw_vertex_array_homo = np.concatenate([raw_vertex_array,np.ones((raw_vertex_array.shape[0],1))],axis=1)
    
    
    rendering_list = []
    light_pos = np.array([0,3,0])
    # image = render_mesh(raw_vertex_array, faces, vertex_normals,light_pos)
    # save_array_as_png(image, "output/output.png")
    
    # exit()
    num_frames = 100
    for i in tqdm.trange(num_frames):
           
        t = i / num_frames 
        #theta = (2*m.pi)*i/100
        theta = (m.pi)*i/100
        # light_pos = np.array([5,0,1])*(1-t)+np.array([-5,0,1])*t
        
        # pos = np.array([4*m.cos(theta),0,4*m.sin(theta)])
        
        target = np.array([0.1,0.1,0.1])
        pos = np.array([0,2*m.cos(0.4*theta),2*m.sin(0.7*theta),]) 
        camera.lookAt(pos=pos, target=target)

        vertex_array_homo = raw_vertex_array_homo @ camera.get_view_matrix().T
        vertex_array = vertex_array_homo[:,:3]
        
        image = render_mesh(vertex_array, faces, vertex_normals,light_pos)
        
        #save_array_as_png(image, "output/output.png")
        #exit()
        rendering_list.append(image)
    os.makedirs("output", exist_ok=True)
    #save_arrays_as_mp4(rendering_list, "output/bunny_nod.mp4",fps=30)
    save_arrays_as_mp4(rendering_list, "output/bunny_tilt.mp4",fps=30)
    
    
    