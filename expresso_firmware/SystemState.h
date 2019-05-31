#ifndef _SYSTEM_STATE_H_
#define _SYSTEM_STATE_H_
#include "WProgram.h"
#include "constants.h"
#include "LevelDetector.h"
#include "TaosLinearArray.h"

class SystemState {
    public:

        SystemState();
        bool setMode(uint16 _mode);
        bool setMode(uint16 _mode, uint8 _channel);
        uint16 getMode();

        bool setChannel(uint8 _channel);
        uint8 getChannel();

        float getLevel(uint8 chan);
        void getBounds(uint8 chan, int32* a, int32* b);
        void setBounds(uint8 chan, int32 a, int32 b);
        void setLevel(uint8 chan, float value); 
        bool setDeviceNumber(uint8 deviceNum); 
        uint8 getDeviceNumber(); 
        void update();

        uint8 deviceNum;
        uint16 mode;                     // Operating mode
        uint8 channel;                   // Channel setting for single channel operation
        float level[constants::NUM_AIN]; // Capillary level data
        float levelRaw[constants::NUM_AIN]; 
        float lastLevel;
        int32 bounds[constants::NUM_AIN][2]; // Debug data (bounds for level detection)
        LevelDetector detector;     // Level detector object  
};

extern const uint16 sysModeStopped;
extern const uint16 sysModeSingleChannel;
extern const uint16 sysModeAllChannels;
extern const uint16 sysModeDebug;

extern SystemState systemState;

#endif
