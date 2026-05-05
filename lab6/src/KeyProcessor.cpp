#include "KeyProcessor.hpp"

KeyProcessor::KeyProcessor() : currentMode(ProcessMode::NORMAL) {}

void KeyProcessor::processKey(int key) {
    if (key == -1) return;

    // Перевіряємо натиснуті цифри
    switch (key) {
        case '1': currentMode = ProcessMode::NORMAL; break;
        case '2': currentMode = ProcessMode::INVERT; break;
        case '3': currentMode = ProcessMode::CANNY; break;
        case '4': currentMode = ProcessMode::BLUR; break;
        case '5': currentMode = ProcessMode::MIRROR; break;
        case '6': currentMode = ProcessMode::CENTER_MIRROR; break;
        default: break;
    }
}

ProcessMode KeyProcessor::getCurrentMode() const {
    return currentMode;
}