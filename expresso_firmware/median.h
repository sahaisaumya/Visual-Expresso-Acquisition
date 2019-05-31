// median.cpp
//
// Functions for finding the median of a set of numbers.
//
// Will Dickson, IO Rodeo  Inc.
//
#ifndef _MEDIAN_H_
#define _MEDIAN_H_
#include <string.h>
#include "WProgram.h"

int medianCmpFunc(const void *xPtr, const void *yPtr);
uint8 getMedian(uint8 *data, uint16 len); 
uint8 getMedianNoModify(uint8 *data, uint16 len); 

#endif
