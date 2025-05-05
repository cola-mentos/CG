import numpy as np

def rotate_y_axis(points, theta):
    """
    将输入的点绕 y 轴旋转指定角度。

    参数:
    points (numpy.ndarray): 形状为 (M, 3) 的点数组。
    theta (float): 旋转角度，范围为 0-360 度。

    返回:
    numpy.ndarray: 旋转后的点数组，形状为 (M, 3)。
    """
    # 将角度转换为弧度
    theta_rad = np.deg2rad(theta)
    
    # 绕 y 轴的旋转矩阵
    rotation_matrix = np.array([
        [np.cos(theta_rad), 0, np.sin(theta_rad)],
        [0, 1, 0],
        [-np.sin(theta_rad), 0, np.cos(theta_rad)]
    ])
    
    # 应用旋转矩阵
    rotated_points = np.dot(points, rotation_matrix.T)
    
    return rotated_points