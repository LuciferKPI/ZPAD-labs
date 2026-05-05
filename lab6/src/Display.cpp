#include "Display.hpp"

Display::Display(const std::string& name, FrameProcessor* processor) : windowName(name) {
    cv::namedWindow(windowName, cv::WINDOW_AUTOSIZE);
    
    // Реєстрація обробників подій миші та повзунка
    cv::setMouseCallback(windowName, FrameProcessor::onMouse, processor);
    cv::createTrackbar("Brightness", windowName, processor->getBrightnessParam(), 100);
}

void Display::show(const cv::Mat& frame) {
    if (!frame.empty()) {
        cv::imshow(windowName, frame);
    }
}

const std::string& Display::getWindowName() const {
    return windowName;
}