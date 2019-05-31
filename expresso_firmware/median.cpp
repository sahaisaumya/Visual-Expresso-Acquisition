// median.cpp
//
// Functions for finding the median of a set of numbers.
//
// Will Dickson, IO Rodeo  Inc.
//
#include <stdlib.h>
#include "median.h"

int medianCmpFunc(const void *xPtr, const void *yPtr) {
    // Comparison function for median computation
    return (int) (*(uint8*)xPtr - *(uint8*)yPtr);
}

uint8 getMedian(uint8 *data, uint16 len) {
    // Computes the medain of the given data. Does not make copy of given data
    // - sorts the data in place when computing the median.

    uint8 median;
    qsort(data, (size_t) len, sizeof(uint8), medianCmpFunc);
    if (len%2 == 0) {
        median = data[len/2-1]/2 + data[len/2]/2;

    }
    else {
        median = data[len/2];
    }
    return median;
}

uint8 getMedianNoModify(uint8 *data, uint16 len) {
    // Computes the medain of the given data. Does not modify the data passed
    // to it.  Insted it makes a copy of the data to use in the median
    // computation.

    uint8 dataCopy[len];
    memcpy(dataCopy,data,len*sizeof(uint8));
    return getMedian(dataCopy,len);
}

