#ifndef _MESSAGE_HANDER_H_
#define _MESSAGE_HANDER_H_
#include <Streaming.h>
#include <SerialReceiver.h>
#include "constants.h"
#include "SystemState.h"
#include "TaosLinearArray.h"

class MessageHandler : public SerialReceiver {
    public:
        void processMsg();
        void msgSwitchYard();
    private:
        void setMode();
        void getMode();
        void setChannel();
        void getChannel();
        void getLevel();
        void getLevels();
        void getPixelData();
        void getBoundData();
        void getWorkingBuffer();
        void getDeviceId();
        void setDeviceId();
        void unSetNormConst();
        void setNormConstFromBuffer();
        void setNormConstFromFlash();
        void saveNormConstToFlash();
};

void sendPixelData(uint8 chan);
void sendWorkingBuffer();

#endif
