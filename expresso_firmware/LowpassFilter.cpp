// LowpassFilter.h
//
// The LowpassFilter class provides a simple implementation of a lowpass filter. 
//
// Cisco Zabala, IO Rodeo.
//
#include "LowpassFilter.h"
#include <string.h>

LowpassFilter::LowpassFilter() {
    _cutoff = constants::cutoff_freq;
    _t_last = 0;
}

void LowpassFilter::apply(uint8* data, uint16 len) {
    uint8 dataFilt[len];  
    float tau;
    float alpha;
    int32 t;
    int32 dt;

    t = millis()*1000;
    dt = t-_t_last;
    _t_last = t;

    dataFilt[0] = data[0];
    for (uint16 i=1; i<len; i++) {
        tau = 1.0/(2*M_PI*_cutoff);
        alpha = dt/(dt  + tau);
        _value = (1-alpha)*_value + alpha*data[i];
        dataFilt[i] = (uint8) _value;
    }
    memcpy(data,dataFilt, len*sizeof(uint8));

}

void setCutoff(int32 _cutoff) {

}
