#include "CameraProvider.hpp"
#include <iostream>

CameraProvider::CameraProvider(int cameraId) {
    cap.open(cameraId, cv::CAP_V4L2);
    
    if (!cap.isOpened()) {
        std::cerr << "Помилка: Не вдалося відкрити камеру!" << std::endl;
        return;
    }
    cap.set(cv::CAP_PROP_FOURCC, cv::VideoWriter::fourcc('M', 'J', 'P', 'G'));
    cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
    cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
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