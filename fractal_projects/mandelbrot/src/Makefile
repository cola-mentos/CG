all : test.cpp include/mandelbrot.h include/window.h include/bitmap.h include/bitmap.cpp
	g++ -o mandelbrot test.cpp include/bitmap.cpp -I include

clean :
	rm -f mandelbrot *.bmp

.PHONY : all clean