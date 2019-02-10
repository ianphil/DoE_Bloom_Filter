#!/usr/bin/evn python

from bitarray import bitarray

def resize_bitarray(barr, new_size):
    b=bitarray(new_size)
    b[:len(barr)]=barr
    return b

b = bitarray()

for item in range(6400):
    if item > len(b):
        b = resize_bitarray(b, item)
        print(len(b))
