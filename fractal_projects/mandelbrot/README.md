### 项目作业——Mandelbrot 集可视化
#### 项目目的
- **科学可视化：** 生成高精度 Mandelbrot 分形图像，展示数学之美
- **性能优化：** 通过并行计算加速图像生成
- **艺术创作：** 实现具有霓虹渐变效果的色彩映射算法
- **使用Makefile构建工具:** 更好地管理项目
#### 功能特性
- 生成高精度Mandelbrot集图像
- 支持自定义图像中心点坐标和观察范围
- 自动生成标准BMP格式图像文件
#### 使用方法
1. 编译项目：
```bash
cd src && make
```
2. 运行
```bash
./程序名 <输出文件名.bmp> <中心点X坐标> <中心点Y坐标> <观察x范围> <观察y范围>
```  
生成以 $(-1.5,-1)$ $(1.5,1)$ 为长方形顶点的mandelbrot集
```bash
./mandelbrot output.bmp 0.0 0.0 1.5 1.0
```
#### 结构
```plaintext
├── mandelbrot
│   ├── README.md 
│   ├── src
│   │   ├── include
│   │   │   ├── bitmap.cpp
|   |   |   ├── windows.h
|   |   |   ├── mandelbrot.h
│   │   │   └── bitmap.h
│   │   ├──  Makefile 
│   │   └──  test.cpp

```