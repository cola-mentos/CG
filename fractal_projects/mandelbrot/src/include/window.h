struct Point2d
{
    double x;
    double y;
};

class Window
{
private:
    Point2d origin = {0.0, 0.0};  // 窗口中心坐标
    double x_dimension = 5.0;     // 水平方向半宽（X轴范围：-x_dim ~ +x_dim）
    double y_dimension = 2.8125;  // 垂直方向半高（Y轴范围：-y_dim ~ +y_dim，默认16:9宽高比）
    int height = 1080;            // 固定像素高度
    int width = 1920;             // 固定像素宽度

public:
    // 默认构造函数（保持16:9宽高比）
    Window() = default;

    // 自定义构造函数（设置独立半宽半高）
    Window(double _ox, double _oy, double _x_dim, double _y_dim)
        : origin{_ox, _oy}, x_dimension(_x_dim), y_dimension(_y_dim) {}

    // 获取基础参数
    double get_x_dimension() const { return x_dimension; }
    double get_y_dimension() const { return y_dimension; }
    int get_height() const { return height; }
    int get_width() const { return width; }
    double get_ox() const { return origin.x; }
    double get_oy() const { return origin.y; }

    // 计算每像素长度（X/Y方向独立）
    double get_lpp_x() const {
        return (2.0 * x_dimension) / width;  // 水平方向每像素长度
    }

    double get_lpp_y() const {
        return (2.0 * y_dimension) / height; // 垂直方向每像素长度
    }

    // 获取实际坐标范围（可选功能）
    void get_x_range(double& x_min, double& x_max) const {
        x_min = origin.x - x_dimension;
        x_max = origin.x + x_dimension;
    }

    void get_y_range(double& y_min, double& y_max) const {
        y_min = origin.y - y_dimension;
        y_max = origin.y + y_dimension;
    }
};