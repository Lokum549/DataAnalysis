#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"
#include <iostream>

int main() {
    CameraProvider camera(0);
    if (!camera.isOpened()) {
        return -1;
    }

    KeyProcessor keyProcessor;
    FrameProcessor frameProcessor;
    Display display("Lab 6 - OpenCV Filters");

    std::cout << "--- Керування ---" << std::endl;
    std::cout << "1 - Звичайний режим" << std::endl;
    std::cout << "2 - Інверсія (bitwise_not)" << std::endl;
    std::cout << "3 - Gaussian blur" << std::endl;
    std::cout << "4 - Canny фільтр" << std::endl;
    std::cout << "5 - Фільтр Собеля" << std::endl;
    std::cout << "6 - Бінаризація" << std::endl;
    std::cout << "7 - Квантизація" << std::endl;
    std::cout << "Стрілки (або W/A/D) - Віддзеркалення" << std::endl;
    std::cout << "ESC - Вихід" << std::endl;

    while (true) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) break;

        ProcessingMode mode = keyProcessor.getCurrentMode();
        cv::Mat processedFrame = frameProcessor.process(frame, mode);

        display.show(processedFrame);

        int key = cv::waitKeyEx(1); 
        if (key != -1) {
            if (!keyProcessor.processKey(key)) {
                break; 
            }
        }
    }

    return 0;
}