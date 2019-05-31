#include <string.h>
#include <Streaming.h>
#include <FlashMemory.h>
#include <SerialReceiver.h>
#include "constants.h"
#include "LevelDetector.h"
#include "TaosLinearArray.h"
#include "MessageHandler.h"
#include "SystemState.h"

MessageHandler handler; 

void setup() {
    linearArray.initialize();
    linearArray.setNormConstFromFlash();
}

void loop() {
    systemState.update();
    handler.processMsg();
}
