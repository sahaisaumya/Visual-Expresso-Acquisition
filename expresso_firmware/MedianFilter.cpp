// MedianFilter.h
//
// The MedianFilter class provides a simple implementatin of a 1D median 
// filter. 
//
// Will Dickson, IO Rodeo.
//
#include "MedianFilter.h"
#include <string.h>
#include "median.h"

MedianFilter::MedianFilter(uint16 _windowLen) {
    setWindowLen(_windowLen);
}

void MedianFilter::setWindowLen(uint16 _windowLen) {
    if (_windowLen%2==0) {
        _windowLen += 1;
    }
    windowLen = _windowLen;
}


void MedianFilter::apply(uint8* data, uint16 len) {
    uint8 median;
    uint8 dataFilt[len];
    uint8 windowData[windowLen];

    for (uint16 i=0; i<len; i++) {
        getWindowData(windowData,data,len,i);
        median = getMedian(windowData,windowLen);
        dataFilt[i] = median;
    }
    memcpy(data,dataFilt, len*sizeof(uint8));
}

void MedianFilter::getWindowData(uint8 *windowData, uint8 *data, uint16 len, uint16 i) {

    int32 k;
    uint16 n=windowLen/2;

    for (uint16 j=0; j<windowLen; j++) {
        // Compute window index in data array. 
        k = i + j - n;
        k = k < 0 ? 0 : k;
        k = k>=len ? (len-1) : k;
        *(windowData+j) = *(data+k);
    }
}
