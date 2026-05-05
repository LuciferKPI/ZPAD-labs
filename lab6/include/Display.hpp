#ifndef DISPLAY_HPP
#define DISPLAY_HPP

#include <opencv2/opencv.hpp>
#include <string>
#include "FrameProcessor.hpp"

class Display {
private:
    std::string windowName;
public:
    Display(const std::string& name, FrameProcessor* processor);
    void show(const cv::Mat& frame);
    const std::string& getWindowName() const;
};

#endif