#include "constants.h"
namespace constants {
    // Taos sensor constants
    const uint8 timerNum = 1;
    const uint32 timerPeriod = 32;
    const int timerChanPwm = 1; 
    const int timerChan1stQtr =2;  
    const int timerChan2ndQtr = 3;
    const int timerChan3rdQtr = 4;
    const uint8 si1Pin = 17; 
    const uint8 clkPin = 27;
    const uint16 exposure = 1; 
    const uint8 ainPin[NUM_AIN] = {11, 10, 9, 8, 7};
    const uint8 normBaseLevel = 232; 
    const uint8 normScaleFact[2] = {3,2};

    // Level detector constants
    const uint16 refLevelSampleNum = 20;
    const uint8 refLevel = 128; 
    const bool reverseBuffer = false;
    const uint16 maxSearchPixel = NUM_PIXEL-167;
    const float peakFitTol = 0.25;
    const uint8 thresholdDeltaLow = 15; 
    const uint8 thresholdDeltaHigh = 28; 
    const int32 thresholdSymm = 15;
    const float lowerThresholdFraction = 0.95;
    const float levelMaxChange = 50.0;

    // Median filter constants
    const uint16 medianFilterWindow = 25; 

    // Derivative filter constants
    const uint16 derivFilterWindow = 21; 
    const uint8 derivFilterShift = 128;
    const uint8 derivFilterScale = 10;

    // Lowpass filter constants
    const int32 cutoff_freq = 10;

    // Device Id
    const uint16 deviceId = 1;
}
