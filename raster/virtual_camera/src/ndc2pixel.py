import numpy as np


def ndc2pixel(ndc_coords, w, h):
    """
    将归一化设备坐标 (NDC) 映射到像素坐标。

    参数:
    ndc_coords (numpy.ndarray): 形状为 (M, 2) 的 NDC 坐标数组，范围为 [-w/h, w/h] x [-1, 1]。
    w (int): 输出图像的宽度。
    h (int): 输出图像的高度。

    返回:
    numpy.ndarray: 形状为 (M, 2) 的像素坐标数组，范围为 [0, w] x [0, h]。
    """
    # 将 NDC 坐标转换到 [0, 1] 范围
    ndc_normalized = np.copy(ndc_coords)
    ndc_normalized[:, 0] = (ndc_coords[:, 0] + w / h) / (2 * w / h)  # x 坐标映射
    ndc_normalized[:, 1] = (ndc_coords[:, 1] + 1) / 2  # y 坐标映射

    # 将 [0, 1] 范围映射到像素坐标
    pixel_coords = np.zeros_like(ndc_normalized)
    pixel_coords[:, 0] = ndc_normalized[:, 0] * w  # x 坐标映射到 [0, w]
    pixel_coords[:, 1] = ndc_normalized[:, 1] * h  # y 坐标映射到 [0, h]

    return pixel_coords


if __name__ == "__main__":
    from save_img import save_array_as_png
    # 输入 NDC 坐标，范围为 [-w/h, w/h] x [-1, 1]
    ndc_coords = np.array(
        [
            [0.0, 0.0],
            [0.5, 0.5],
        ]
    ) 

    # 图像宽度和高度
   

    
