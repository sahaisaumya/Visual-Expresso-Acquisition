// TaosLinearArray.cpp
//
// The TaosLinearArray class provides an interface to the TAOS Linear Array
// Sensors (e.g. TSL1406) for use with LeafLabs Maple, Maple Mini, and Maple
// Native microcontroller boards. 
//
// Will Dickson, IO Rodeo Inc.
//
#include "TaosLinearArray.h"

// Hardware timer 
HardwareTimer timer(constants::timerNum);

// TaosLinearArray class methods
// ----------------------------------------------------------------------------
TaosLinearArray::TaosLinearArray()
{
    si1Pin = constants::si1Pin;
    clkPin = constants::clkPin;
    ainPin = (uint8*) constants::ainPin;
    setExposure(constants::exposure);
    normBaseLevel = constants::normBaseLevel;

    clkCnt = 0;
    ainCnt = 0;
    noInterrupts();
    startSignal = false;
    readInProgress = false;
    dataReadySignal = false;
    interrupts();

    for (int i=0; i<numAin; i++) {
        for (int j=0; j<numPixel; j++) {
            buffer[i][j] = 0;
            normConst[i][j] = normBaseLevel;
        }
        normScaleFact[i][0] = 1;
        normScaleFact[i][1] = 1;
    }
}

void TaosLinearArray::initialize() {
    // Initializes the GPIO for the sensor and the hardware timer used
    // by the sensor to pace the readings.
    initializeGPIO();
    initializeTimer(timer,constants::timerPeriod);
}

void TaosLinearArray::initializeGPIO() {
    // Initializes the GPIO for the linear array sensor. The si1 pin is
    // set to digital output, the clk pin is set to a pwm output, and the
    // analog input pins are set to analog inputs.

    pinMode(si1Pin, OUTPUT);
    pinMode(clkPin, PWM);
    for (int i=0; i<numAin; i++) {
        pinMode(ainPin[i], INPUT_ANALOG);
    }
    digitalWrite(si1Pin, LOW);
    digitalWrite(clkPin, LOW);
}

void TaosLinearArray::setExposure(uint16 val) {
    // Sets the exposure value for the linear array sensor. The exposure
    // setting determines the number of additional clock ticks which occur
    // after all sensor data has been before a new read is initialed.
    clkCntMax = numPixel + val + 1;
}

uint16 TaosLinearArray::getExposure() {
    // Returns the current exposure setting.
    return clkCntMax - numPixel - 1;
}

void TaosLinearArray::readData() {
    // Initiates a read into the sensor buffer and waits for the read to
    // complete.
    startDataRead();
    while (!dataReady()) {};
}

void TaosLinearArray::unSetNormConst() {
    // Unset sets the normalization constants - so that the data in the buffer
    // is the raw sensor data.
    for (int i=0; i<numAin; i++) {
        unSetNormConst(i);
    }
}

void TaosLinearArray::unSetNormConst(uint8 chanNum) {
    if (chanNum < numAin) {
        for (int j=0; j<numPixel; j++) {
            normConst[chanNum][j] = normBaseLevel; 
        }
        normScaleFact[chanNum][0] = 1;
        normScaleFact[chanNum][1] = 1;
    }
}

void TaosLinearArray::setNormConstFromBuffer() {
    // Sets the normalization constant values, for all channels, based on current
    // values in the acquisition buffer.  
    for (uint8 i=0; i<numAin; i++) {
        setNormConstFromBuffer(i);
    }
}

void TaosLinearArray::setNormConstFromBuffer(uint8 chanNum) {
    // Sets the pixel normalization constant values, for the given chan, to the
    // current values in the acquisition buffer.
    if (chanNum < numAin) {
        for (uint16 j=0; j<numPixel; j++) {
            normConst[chanNum][j] = buffer[chanNum][j];
        }
        normScaleFact[chanNum][0] = constants::normScaleFact[0];
        normScaleFact[chanNum][1] = constants::normScaleFact[1];
    }
}

void TaosLinearArray::setNormConstFromFlash() {
    // Sets the pixel normalization constants, for all channels, from the values
    // stored in flash memory. 
    for (uint8 i=0; i<numAin; i++) {
        setNormConstFromFlash(i);
    }
}

void TaosLinearArray::setNormConstFromFlash(uint8 chanNum) {
    // Sets the normalization constants for the given channel from the values
    // stored in flash memory. 
    uint16 ind0;
    uint16 ind1;
    uint8 data0;
    uint8 data1;
    uint16 maxAddress;
    if ((chanNum < numAin) && (chanNum < flashMemory.numPages)) {
        if (numPixel%2==0) {
            maxAddress = numPixel/2;
        }
        else {
            maxAddress = numPixel/2 + 1;
        }
        if (maxAddress <= flashMemory.maxAddress) {
            for (uint16 address=0; address<maxAddress; address++) {
                ind0 = 2*address;
                ind1 = 2*address + 1;
                flashMemory.readData(chanNum,address,data0,data1);
                normConst[chanNum][ind0] = data0;
                normConst[chanNum][ind1] = data1;
            }
            normScaleFact[chanNum][0] = constants::normScaleFact[0];
            normScaleFact[chanNum][1] = constants::normScaleFact[1];
        }
    }
}

void TaosLinearArray::saveNormConstToFlash() {
    // Saves the normalization constants, for all channels, to flash
    // memory.
    for (uint8 i=0; i<numAin; i++) {
        saveNormConstToFlash(i);
    }
}

void TaosLinearArray::saveNormConstToFlash(uint8 chanNum) {
    // Saves the normalization constants, for the given channel,  to flash
    // memory.
    uint16 ind0;
    uint16 ind1;
    uint8 data0;
    uint8 data1;
    uint16 maxAddress;
    if ((chanNum < numAin) && (chanNum < flashMemory.numPages)) {
        flashMemory.erasePage(chanNum);
        if (numPixel%2==0) {
            maxAddress = numPixel/2;
        }
        else {
            maxAddress = numPixel/2 + 1;
        }
        if (maxAddress <= flashMemory.maxAddress) {
            for (uint16 address=0; address<maxAddress; address++) {
                ind0 = 2*address;
                ind1 = 2*address + 1;
                data0 = normConst[chanNum][ind0];
                data1 = normConst[chanNum][ind1];
                flashMemory.writeData(chanNum,address,data0,data1);
            }
        }
    }
} 

void TaosLinearArray::setDeviceId(uint32 deviceId) {
    uint8 pageNum = numAin;
    // deviceId = 0x78765432;
    if (pageNum < flashMemory.numPages) {
        flashMemory.erasePage(pageNum);
        flashMemory.writeData(pageNum,0,deviceId&0xFFFF);
        flashMemory.writeData(pageNum,1,(deviceId>>16)&0xFFFF);
    }
}
 
uint32 TaosLinearArray::getDeviceId() {
    uint8 pageNum = numAin;
    uint16 id_lsb;
    uint16 id_msb;
    flashMemory.readData(pageNum,0,id_lsb);
    flashMemory.readData(pageNum,1,id_msb);
    //id_lsb = 0xFFFF; // 1
    //id_msb = 0x0000; // Nothing
    _deviceId = (uint32) id_msb<<16;
    _deviceId |= (uint32) id_lsb;
    return _deviceId;
}

void TaosLinearArray::startDataRead() {
    // Sets the start signal which signals that data should be read into
    // the sensor buffer.
    noInterrupts();
    ainCnt = 0;
    dataReadySignal = false;
    startSignal = true;
    interrupts();
}

bool TaosLinearArray::dataReady() {
    // Checks the data ready signal which indicates that the data int the
    // sensor buffer is ready - i.e., that the last read has completed.
    return dataReadySignal;
}

void TaosLinearArray::timerUpdate1stQtr() {
    // Update function for the 1st quater of timer period. Set the SI 
    // (read initiation) pin low on the 2nd (clkCnt=1) cycle of a read from 
    // the sensor.
    if (clkCnt == 1) {
        digitalWrite(si1Pin, LOW); 
    }
}

void TaosLinearArray::timerUpdate2ndQtr() {
    // Update function for the 2nd quater of the timer period. Reads data
    // from the sensor and applies gain normalization to the values.
    uint16 pixelValue;
    uint16 normValue;
    uint16 normPixelValue;
    int16  scaledPixelValue;

    if ((clkCnt >= 1) && (clkCnt < (numPixel+1))) {

        if (readInProgress) {
            // Read pixel value, normalize and scale
            pixelValue = analogRead(ainPin[ainCnt]);
            normValue = (uint16) normConst[ainCnt][clkCnt-1];
            normPixelValue = pixelValue*normBaseLevel/normValue;
            // Shift offset to zero and scale result and add back in offset
            scaledPixelValue = (int16) normPixelValue - (int16) (normBaseLevel<<4);
            scaledPixelValue = (normScaleFact[ainCnt][0]*scaledPixelValue)/normScaleFact[ainCnt][1];
            scaledPixelValue = scaledPixelValue + (int16) (normBaseLevel<<4);
            if (scaledPixelValue < 0) {
                scaledPixelValue = 0;
            }
            if (scaledPixelValue > (255<<4)) {
                scaledPixelValue = (255<<4);
            }
            buffer[ainCnt][clkCnt-1] = (uint8) (scaledPixelValue >> 4);
            if (clkCnt == numPixel) {
                ainCnt++;
                if (ainCnt >= numAin) {
                    // DEBUG - check zeroing of ainCnt  
                    readInProgress = false;
                    dataReadySignal = true;
                }
            }  
        } // if (readInProgress) 
    }
}

void TaosLinearArray::timerUpdate3rdQtr() {
    // Update function for 3rd quarter of timer period. Sets the initial
    // SI pin High to initial read from sensor when the clock count is 0. 
    // Registers the startSignal to begin a read of data into the buffer. 

    // Initiate read from sensor
    if (clkCnt == 0) {
        digitalWrite(si1Pin, HIGH);
    }

    // Update clock count and start new reading if start signal has been
    // recieved.
    clkCnt++;
    if (clkCnt >= clkCntMax) { 
        clkCnt = 0;
        if (startSignal) {
            startSignal = false;
            readInProgress = true;
        }
    }
}


// Hardware timer functions
// ----------------------------------------------------------------------------

void initializeTimer(HardwareTimer &timer, uint32 timerPeriod) {
    // Initializes the hardware timer used by the linear array sensor. 
    uint16 overflow;
    timer.pause();
    timer.setCount(0);
    timer.setPeriod(timerPeriod);
    timer.refresh();
    overflow = timer.getOverflow();
    timer.setCompare(constants::timerChanPwm,2*overflow/4); // PWM output on clk pin
    timer.setCompare(constants::timerChan1stQtr,1*overflow/4); // 1st Qtr 
    timer.setCompare(constants::timerChan2ndQtr,2*overflow/4); // 2nd Qtr
    timer.setCompare(constants::timerChan3rdQtr,3*overflow/4); // 3rd Qtr
    timer.attachInterrupt(constants::timerChan1stQtr, timerInterrupt1stQtr);
    timer.attachInterrupt(constants::timerChan2ndQtr, timerInterrupt2ndQtr); 
    timer.attachInterrupt(constants::timerChan3rdQtr, timerInterrupt3rdQtr); 
    timer.refresh();
    timer.resume();
}

void timerInterrupt1stQtr() {
    // Interrupt hander which is called during the 1st quater of a timer period.
    linearArray.timerUpdate1stQtr();
}

void timerInterrupt2ndQtr() {
    // Interrupt handler which is called during the  2nd quater of a timer period.
    linearArray.timerUpdate2ndQtr();
}

void timerInterrupt3rdQtr() {
    // Interrupt handler which is called during the 3rd quater of a timer period.
    linearArray.timerUpdate3rdQtr();
}


TaosLinearArray linearArray;
