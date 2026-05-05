#ifndef KEY_PROCESSOR_HPP
#define KEY_PROCESSOR_HPP

enum class ProcessMode {
    NORMAL,
    INVERT,
    CANNY,
    BLUR,
    MIRROR,
    CENTER_MIRROR
};

class KeyProcessor {
private:
    ProcessMode currentMode;
public:
    KeyProcessor();
    void processKey(int key);
    ProcessMode getCurrentMode() const;
};

#endif