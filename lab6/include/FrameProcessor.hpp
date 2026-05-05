#ifndef FRAME_PROCESSOR_HPP
#define FRAME_PROCESSOR_HPP

#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"
#include <vector>

class FrameProcessor {
private:
    int brightness;
    std::vector<cv::Point> clickPoints;
    int64 lastTick;

public:
    FrameProcessor();
    cv::Mat process(const cv::Mat& inputFrame, ProcessMode mode);
    
    static void onMouse(int event, int x, int y, int flags, void* userdata);
    void addClickPoint(int x, int y);
    void clearClickPoints();
    
    int* getBrightnessParam();
};

#endif