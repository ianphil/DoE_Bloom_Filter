#!/usr/bin/env python

import mmh3
from bitarray import bitarray

size=10000
hash_pass_count=1
b=bitarray(size)

with open('../resources/present.txt', 'r') as fp:
    present=fp.readlines()
with open('../resources/absent.txt', 'r') as fp:
    absent=fp.readlines()

for p in present:
    for i in range(hash_pass_count):
        p_hash=mmh3.hash(p, i)%size
        b[p_hash]=True

false_count=0
for a in absent:
    digest=[]
    for i in range(hash_pass_count):
        a_hash=mmh3.hash(a, i)%size
        a_present=b[a_hash]
        digest.append(a_present)
        if not a_present:            
            break
        else:
            if len(digest) == hash_pass_count:
                false_count+=1

percent_false=(false_count/len(absent))*100

print(str(percent_false) + '% are false positives: count is - ' + str(false_count))
