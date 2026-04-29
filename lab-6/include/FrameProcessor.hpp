#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
public:
    FrameProcessor();
    cv::Mat process(const cv::Mat& inputFrame, ProcessingMode mode);
};