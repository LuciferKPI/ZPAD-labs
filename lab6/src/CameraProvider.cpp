#include "CameraProvider.hpp"
#include <iostream>

CameraProvider::CameraProvider(int deviceId) {
    // Використовуємо лінуксовий бекенд
    cap.open(deviceId, cv::CAP_V4L2);
    
    // Залишаємо малу роздільну здатність, щоб USB-шина віртуалки на якій я перевіряв не задихалася
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);

    if (!cap.isOpened()) {
        std::cerr << "Error: Could not open camera" << std::endl;
    }
}

CameraProvider::~CameraProvider() {
    if (cap.isOpened()) {
        cap.release();
    }
}

cv::Mat CameraProvider::getFrame() {
    cv::Mat frame;
    cap >> frame;
    return frame;
}

bool CameraProvider::isOpened() const {
    return cap.isOpened();
}