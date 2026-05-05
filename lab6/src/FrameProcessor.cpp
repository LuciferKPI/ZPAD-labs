#include "FrameProcessor.hpp"

FrameProcessor::FrameProcessor() : brightness(50), lastTick(cv::getTickCount()) {}

cv::Mat FrameProcessor::process(const cv::Mat& inputFrame, ProcessMode mode) {
    if (inputFrame.empty()) return inputFrame;

    cv::Mat result;
    
    switch (mode) {
        case ProcessMode::INVERT:
            cv::bitwise_not(inputFrame, result);
            break;
        case ProcessMode::CANNY:
            cv::cvtColor(inputFrame, result, cv::COLOR_BGR2GRAY);
            cv::Canny(result, result, 50, 150);
            cv::cvtColor(result, result, cv::COLOR_GRAY2BGR);
            break;
        case ProcessMode::BLUR:
            cv::GaussianBlur(inputFrame, result, cv::Size(15, 15), 0);
            break;
        case ProcessMode::MIRROR:
            // Звичайне віддзеркалення (1 означає по горизонталі)
            cv::flip(inputFrame, result, 1);
            break;
        case ProcessMode::CENTER_MIRROR: {
            // Ефект симетрії (дві правих частини)
            inputFrame.copyTo(result);
            int width = result.cols;
            int height = result.rows;
            int mid = width / 2;
            
            // Вирізаємо праву половину кадру
            cv::Mat rightHalf = inputFrame(cv::Rect(mid, 0, width - mid, height));
            cv::Mat flippedRight;
            // Віддзеркалюємо її
            cv::flip(rightHalf, flippedRight, 1);
            // Вставляємо віддзеркалену праву частину на місце лівої
            flippedRight.copyTo(result(cv::Rect(0, 0, mid, height)));
            break;
        }
        case ProcessMode::NORMAL:
        default:
            inputFrame.copyTo(result);
            break;
    }

    // Регулювання яскравості
    int brightnessOffset = (brightness - 50) * 2;
    result.convertTo(result, -1, 1, brightnessOffset);

    // Малювання кіл
    for (const auto& pt : clickPoints) {
        cv::circle(result, pt, 15, cv::Scalar(0, 0, 255), -1);
    }

    // FPS та інструкції
    double fps = cv::getTickFrequency() / (cv::getTickCount() - lastTick);
    lastTick = cv::getTickCount();

    // Виводимо текст у два рядки, щоб не перекривати екран
    cv::putText(result, "1:Norm 2:Inv 3:Can 4:Blur 5:Mir 6:Split | FPS: " + std::to_string((int)fps), 
                cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 255, 0), 2);
    cv::putText(result, "LMB: Draw Circle | RMB: Clear Circles", 
                cv::Point(10, 55), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 255, 255), 2);

    return result;
}

void FrameProcessor::addClickPoint(int x, int y) {
    if (clickPoints.size() > 20) {
        clickPoints.erase(clickPoints.begin());
    }
    clickPoints.push_back(cv::Point(x, y));
}

void FrameProcessor::clearClickPoints() {
    clickPoints.clear();
}

int* FrameProcessor::getBrightnessParam() {
    return &brightness;
}

void FrameProcessor::onMouse(int event, int x, int y, int flags, void* userdata) {
    FrameProcessor* fp = reinterpret_cast<FrameProcessor*>(userdata);
    if (fp) {
        if (event == cv::EVENT_LBUTTONDOWN) {
            // Ліва кнопка - малювати
            fp->addClickPoint(x, y);
        } else if (event == cv::EVENT_RBUTTONDOWN) {
            // Права кнопка - стерти все
            fp->clearClickPoints();
        }
    }
}