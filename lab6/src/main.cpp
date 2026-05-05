#include <iostream>
#include "CameraProvider.hpp"
#include "KeyProcessor.hpp"
#include "FrameProcessor.hpp"
#include "Display.hpp"

int main() {
    // Ініціалізація камери
    CameraProvider camera(0);
    if (!camera.isOpened()) {
        std::cerr << "Помилка: Не вдалося підключитися до камери!" << std::endl;
        return -1;
    }

    KeyProcessor keyProcessor;
    FrameProcessor frameProcessor;
    Display display("ZPAD Lab 6 - OpenCV", &frameProcessor);

    int key = 0;
    
    // Головний цикл програми, вихід по ESC (код 27)
    while (key != 27) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) {
            std::cerr << "Помилка: Отримано порожній кадр!" << std::endl;
            break;
        }

        keyProcessor.processKey(key);
        cv::Mat processedFrame = frameProcessor.process(frame, keyProcessor.getCurrentMode());
        display.show(processedFrame);

        key = cv::waitKey(30);
    }

    return 0;
}