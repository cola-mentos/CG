#include <iostream>
#include <cstdlib>
#include <cmath>
#include <omp.h>
#include "window.h"
#include "mandelbrot.h"
#include "bitmap.h"

constexpr int MAX_ITER = 100;
constexpr double COLOR_SPEED = 0.2;
constexpr double GLOW_INTENSITY = 1.5;
constexpr double DEPTH_EFFECT = 0.01;

void get_color(double value, char& b, char& g, char& r) {
    if (value >= MAX_ITER) {
        r = 25;   g = 40;   b = 100;
        return;
    }

    const double hue = fmod(value * COLOR_SPEED, 1.0);
    const double glow = GLOW_INTENSITY * exp(-value / 80.0);
    
    double red = glow * (0.2 + 0.8 * sin(hue * 6.3 + 2.1));
    double green = glow * (0.6 + 0.4 * sin(hue * 5.7 + 1.5)) * (0.8 + 0.2 * sin(value * 0.2));
    double blue = glow * (0.8 + 0.2 * sin(hue * 4.9 + 0.5)) * (1.0 - 0.4 * cos(value * 0.3));

    const double depth = 1.0 - exp(-value * DEPTH_EFFECT);
    red = red * (1 - depth) + depth * 0.15 * (1 + sin(value * 0.2));
    green = green * (1 - depth) + depth * 0.18 * (1 + cos(value * 0.25));
    blue = blue * (1 - depth) + depth * 0.35 * (1 + sin(value * 0.3));

    auto clamp = [](double v) { return v < 0 ? 0 : v > 1 ? v : v; };
    red = pow(clamp(red), 0.9);
    green = pow(clamp(green), 1.0);
    blue = pow(clamp(blue), 1.2);

    r = static_cast<char>(red * 255);
    g = static_cast<char>(green * 255);
    b = static_cast<char>(blue * 255);
}

int main(int argc, char *argv[]) {
    if (argc < 6) {  
        std::cerr << "Usage: " << argv[0] 
                  << " filename ox oy x_dimension y_dimension" << std::endl;
        exit(-1);
    }

    Window win(
        std::atof(argv[2]),  // ox
        std::atof(argv[3]),  // oy
        std::atof(argv[4]),  // x_dimension
        std::atof(argv[5])   // y_dimension
    );

    const int width = win.get_width();
    const int height = win.get_height();
    
    const double lpp_x = win.get_lpp_x();
    const double lpp_y = win.get_lpp_y();

    char* cache = new char[width * height * 3];

    #pragma omp parallel for collapse(2) schedule(dynamic)
    for (int j = 0; j < height; j++) {
        for (int i = 0; i < width; i++) {
            const double ox = win.get_ox() - win.get_x_dimension();
            const double oy = win.get_oy() - win.get_y_dimension();
            
            const double x = ox + lpp_x * i;
            const double y = oy + lpp_y * j;
            const int pos = (j * width + i) * 3;

            Manderbrot man({0.0, 0.0}, MAX_ITER, {x, y});
            while (!man.stop_criterion() && !man.is_disconvergence()) {
                man.forward_step();
            }

            const int raw_iter = man.get_iteration_times();
            const double zn = std::abs(man.get_iteration_point());
            const double smooth_iter = (raw_iter < MAX_ITER) ? 
                raw_iter - log2(zn + 1e-9) : raw_iter;

            char blue, green, red;
            get_color(smooth_iter, blue, green, red);
            
            cache[pos]   = blue;
            cache[pos+1] = green;
            cache[pos+2] = red;
        }
    }

    build_bmp(argv[1], width, height, cache);
    delete[] cache;
    return 0;
}