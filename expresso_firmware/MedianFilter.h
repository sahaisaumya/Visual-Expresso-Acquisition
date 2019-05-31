// MedianFilter.h
//
// The MedianFilter class provides a simple implementatin of a 1D median 
// filter. 
//
// Will Dickson, IO Rodeo.
//
#ifndef _MEDIAN_FILTER_H_
#define _MEDIAN_FILTER_H_
#include "WProgram.h"

class MedianFilter {
    public:
        MedianFilter(uint16 _windowLen=5);
        void apply(uint8 *data, uint16 len);
        void setWindowLen(uint16 _windowLen);
    private:
        uint16 windowLen;
        void getWindowData(uint8 *windowData, uint8 *data, uint16 len, uint16 i);
};

#endif
