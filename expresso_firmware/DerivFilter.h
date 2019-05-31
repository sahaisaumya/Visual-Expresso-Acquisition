// DerivFilter.h
//
// Implements a simple central differences derivative filter. 
//
// Will Dickson, IO Rodeo Inc.
//
#ifndef _DERIV_FILTER_H_ 
#define _DERIV_FILTER_H_
#include "WProgram.h"

class DerivFilter {
    public:
        DerivFilter(uint16 _windowLen=5, uint8 _scale=10, uint8 _shift=128);
        void apply(uint8 *data, uint16 len);
        void setWindowLen(uint16 _windowLen);
        void setScale(uint8 _scale);
        void setShift(uint8 _shift);
        void setThreshold(uint16 x_val,uint16 y_val);
        uint16* getThreshold();
    private:
        uint16 threshold[2];
        uint8 shift;
        uint8 scale;
        uint16 windowLen;
};

#endif
