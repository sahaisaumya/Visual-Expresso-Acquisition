// LowpassFilter.h
//
// The LowpassFilter class provides a simple implementation of a lowpass filter. 
//
// Cisco Zabala, IO Rodeo.
//
#define _USE_MATH_DEFINES
#ifndef _LOWPASS_FILTER_H_
#define _LOWPASS_FILTER_H_
#include "WProgram.h"
#include "constants.h"

class LowpassFilter {
    public:
        LowpassFilter();
        void apply(uint8 *data, uint16 len);
        void setCutoff(int32 _cutoff);
    private:
        int32 _cutoff;
        uint8 _value;
        int32 _t_last;
};

#endif
