#!/usr/bin/env python

import mmh3
from bitarray import bitarray

size=20000
b=bitarray(size)

with open('resources/present.txt', 'r') as fp:
    present=fp.readlines()
with open('resources/absent.txt', 'r') as fp:
    absent=fp.readlines()

for p in present:
    p_hash=mmh3.hash(p)%size
    b[p_hash]=True

false_count=0
for a in absent:
    a_hash=mmh3.hash(a)%size
    a_present=b[a_hash]
    if a_present:
        false_count+=1

percent_false=(false_count/len(absent))*100

print(str(percent_false) + '% are false positives: count is - ' + str(false_count))
