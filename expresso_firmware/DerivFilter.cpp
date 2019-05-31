// DerivFilter.cpp
//
// Implements a simple central differences derivative filter. 
//
// Will Dickson, IO Rodeo Inc.
//
#include "DerivFilter.h"
#include <string.h>
#include "constants.h"

DerivFilter::DerivFilter(uint16 _windowLen, uint8 _scale, uint8 _shift) {
    shift = _shift;
    scale = _scale;
    setWindowLen(_windowLen);
}

void DerivFilter::setWindowLen(uint16 _windowLen) {
    windowLen = _windowLen;
}

void DerivFilter::setScale(uint8 _scale) {
    scale = _scale;
}

void DerivFilter::setShift(uint8 _shift) {
    shift = _shift;
}

void DerivFilter::setThreshold(uint16 x_val, uint16 y_val){
    threshold = {x_val, y_val};
}

uint16* DerivFilter::getThreshold() {
    return threshold;
}

void DerivFilter::apply(uint8 *data, uint16 len) {
    int32 kNeg;
    int32 kPos;
    uint16 maxValueX = 0;
    uint16 maxValueY = 0;
    uint16 n = windowLen/2;
    uint8 dataFilt[len];
    float value;
    float scaleFact = (2*(float)scale)/((float)windowLen - 1.0);

    for (uint16 i=0; i<len; i++) {
        kNeg = i-n;
        kPos = i+n;
        if (kNeg < 0) {
            value = (float) shift;
        }
        else if (kPos >=len) {
            value = (float) shift;
        }
        else {
            value = (scaleFact*(float)data[kPos] + ((float) shift - (float)scaleFact*data[kNeg]));
        }
        dataFilt[i] = (uint8) value;

        // Search for the max if the index is in the searchable region.
        if (i < constants::maxSearchPixel) {
            if (value > maxValueY) {
                maxValueY = (uint16) value;
                maxValueX = i;
            }
        }
    }
    setThreshold(maxValueX,maxValueY);
    memcpy(data,dataFilt,len*sizeof(uint8));
}
