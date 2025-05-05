import numpy as np
from PIL import Image


def save_array_as_png(array, filename):
    """
    将给定的 NumPy 数组保存为 PNG 图像。

    参数:
    array (numpy.ndarray): 形状为 (width, height, 3) 的 NumPy 数组，数值范围为 0-1。
    filename (str): 保存的文件名（包括路径和扩展名，例如 'output.png'）。
    """
    # 将数组的值从 0-1 范围转换为 0-255 范围，并转换为 uint8 类型

    array = np.flip(array, axis=1)
    array = np.transpose(array, (1, 0, 2))

    array_uint8 = (array * 255).astype(np.uint8)

    # 使用 PIL 创建图像对象
    image = Image.fromarray(array_uint8, "RGB")

    # 保存图像为 PNG 文件
    image.save(filename)


# 示例用法
if __name__ == "__main__":
    # 创建一个示例的 RGB 图像数组
    width, height = 1080, 720

    example_array = np.zeros((width, height, 3), dtype=np.float32)
    example_array[:, :, :] = 1

    # 保存为 PNG 文件
    save_array_as_png(example_array, "output.png")
