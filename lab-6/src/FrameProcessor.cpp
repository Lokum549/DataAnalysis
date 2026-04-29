#include "FrameProcessor.hpp"

FrameProcessor::FrameProcessor() {}

cv::Mat FrameProcessor::process(const cv::Mat& input, ProcessingMode mode) {
    if (input.empty()) return input;

    cv::Mat output;
    
    switch (mode) {
        case ProcessingMode::NORMAL:
            output = input.clone();
            break;
            
        case ProcessingMode::INVERT:
            cv::bitwise_not(input, output);
            break;
            
        case ProcessingMode::BLUR: 
            cv::GaussianBlur(input, output, cv::Size(15, 15), 0);
            break;
            
        case ProcessingMode::CANNY: 
            cv::cvtColor(input, output, cv::COLOR_BGR2GRAY);
            cv::Canny(output, output, 50, 150);
            break;
            
        case ProcessingMode::SOBEL: { 
            cv::Mat gray, grad_x, grad_y, abs_grad_x, abs_grad_y;
            cv::cvtColor(input, gray, cv::COLOR_BGR2GRAY);
            cv::Sobel(gray, grad_x, CV_16S, 1, 0, 3);
            cv::Sobel(gray, grad_y, CV_16S, 0, 1, 3);
            cv::convertScaleAbs(grad_x, abs_grad_x);
            cv::convertScaleAbs(grad_y, abs_grad_y);
            cv::addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0, output);
            break;
        }
        
        case ProcessingMode::BINARY: 
            cv::cvtColor(input, output, cv::COLOR_BGR2GRAY);
            cv::threshold(output, output, 128, 255, cv::THRESH_BINARY);
            break;
            
        case ProcessingMode::QUANTIZE: 
            output = input.clone();
            output /= 64; 
            output *= 64;
            output += 32;
            break;
            
        case ProcessingMode::FLIP_H: 
            cv::flip(input, output, 1);
            break;
            
        case ProcessingMode::FLIP_V:
            cv::flip(input, output, 0);
            break;
    }
    
    return output;
}