import numpy as np
import imageio
import tqdm


def save_arrays_as_mp4(arrays, filename, fps=30):
    """
    将给定的 NumPy 数组列表保存为 MP4 视频文件。

    参数:
    arrays (list of numpy.ndarray): 包含形状为 (height, width, 3) 的 NumPy 数组的列表，数值范围为 0-1。
    filename (str): 保存的文件名（包括路径和扩展名，例如 'output.mp4'）。
    fps (int): 视频的帧率（默认 30）。
    """
    # 检查数组列表是否为空
    if not arrays:
        raise ValueError("输入的数组列表不能为空")

    # 将数组的值从 0-1 范围转换为 0-255 范围，并转换为 uint8 类型
    arrays_uint8 = []
    for array in arrays:
        array = np.flip(array, axis=1)
        array = np.transpose(array, (1, 0, 2))
        array = (array * 255).astype(np.uint8)

        arrays_uint8.append(array)

    # 使用 imageio 保存为 MP4 文件
    imageio.mimsave(filename, arrays_uint8, fps=fps)


# 示例用法
if __name__ == "__main__":
    # 创建一个示例的 NumPy 数组列表
    width, height = 720, 480
    num_frames = 100
    rendering_list = []
    for i in range(num_frames):
        t = i / num_frames

       

        image = np.zeros((width, height, 3), dtype=np.float32)

        image[:int(width * t),  :200, 1] = 1.0

        rendering_list.append(image)

    # # 保存为 MP4 文件
    save_arrays_as_mp4(rendering_list, "output.mp4", fps=30)
