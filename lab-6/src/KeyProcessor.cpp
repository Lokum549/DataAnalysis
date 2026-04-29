#include "KeyProcessor.hpp"

KeyProcessor::KeyProcessor() : currentMode(ProcessingMode::NORMAL) {}

bool KeyProcessor::processKey(int key) {
    if (key == 27) return false; 

    switch (key) {
        case '1': currentMode = ProcessingMode::NORMAL; break;
        case '2': currentMode = ProcessingMode::INVERT; break;
        case '3': currentMode = ProcessingMode::BLUR; break;
        case '4': currentMode = ProcessingMode::CANNY; break;
        case '5': currentMode = ProcessingMode::SOBEL; break;
        case '6': currentMode = ProcessingMode::BINARY; break;
        case '7': currentMode = ProcessingMode::QUANTIZE; break;

        case 65361: 
        case 81:    
        case 'a': 
            currentMode = ProcessingMode::FLIP_H; break;
            
        case 65362: 
        case 82:   
        case 'w': 
            currentMode = ProcessingMode::FLIP_V; break;
            
        case 65363: 
        case 83:    
        case 'd':
            currentMode = ProcessingMode::NORMAL; break;
    }
    return true;
}

ProcessingMode KeyProcessor::getCurrentMode() const {
    return currentMode;
}