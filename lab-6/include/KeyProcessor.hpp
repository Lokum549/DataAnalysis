#pragma once

enum class ProcessingMode {
    NORMAL,
    INVERT,
    BLUR,
    CANNY,
    SOBEL,
    BINARY,
    QUANTIZE,
    FLIP_H,
    FLIP_V
};

class KeyProcessor {
private:
    ProcessingMode currentMode;
public:
    KeyProcessor();
    bool processKey(int key); 
    ProcessingMode getCurrentMode() const;
};