import numpy as np
class Camera:
    def __init__(self, R=None, T=True):
        pass
    
    def lookAt(self, pos=np.array([4,0,0]), target=np.array([0,0,0])):
        view_dir= target - pos

        z = -view_dir
        z = z/np.linalg.norm(z)

        y_approx = np.array([0,1,0])

        x = np.cross(y_approx, z)
        x = x/np.linalg.norm(x)

        y = np.cross(z,x)
        y = y/np.linalg.norm(y)

        mat = np.zeros((4,4),dtype=np.float32)
        mat[:3,0] = x
        mat[:3,1] = y
        mat[:3,2] = z
        mat[:3,3] = pos
        mat[3,3] = 1
        self.view_mat = np.linalg.inv(mat)
    
    def get_view_matrix(self):
        return self.view_mat