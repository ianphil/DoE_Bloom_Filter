#!/usr/bin/env python
import os
import gc
import psutil
from bitarray import bitarray

proc = psutil.Process(os.getpid())
gc.collect()
mem0 = proc.memory_info().rss
print(mem0)

b=bitarray(64000000)
b[9] = True
#print(b)
mem1 = proc.memory_info().rss
print(mem1)

a=120000000

if a > len(b):
    b2 = bitarray(a)
    b2[0:len(b)]=b
    del b
    mem2 = proc.memory_info().rss
    print(mem2)
    gc.collect()
    mem3 = proc.memory_info().rss
    print(mem3)

#print(b2)

pd = lambda x2, x1: 100.0 * (x2 - x1) / mem0
print("Allocation: %0.2f%%" % pd(mem1, mem0))
print ("Unreference: %0.2f%%" % pd(mem2, mem1))
print ("Collect: %0.2f%%" % pd(mem3, mem2))
print ("Overall: %0.2f%%" % pd(mem3, mem0))

# https://pypi.org/project/memory-profiler/