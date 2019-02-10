#!/usr/bin/env python

import mmh3
from bitarray import bitarray

# HYPO: Increase size will decrease FP
# HYPO: Increase hash pass will decrease FP
# HYPO: Minimize size and hash while maintaining low FP will increase speed

class Size_Bloom(object):
    def __init__(self, item_count):
        self.size=item_count
        self.present_data=self.get_present_data()
        self.absent_data=self.get_absent_data()
        self.ba=bitarray(self.size)

    def add(self, item):
        h=mmh3.hash(item)%self.size
        self.ba[h]=True

    def check(self, item):
        h=mmh3.hash(item)%self.size
        return self.ba[h]

    @classmethod
    def get_present_data(self):
        with open('resources/present.txt', 'r') as fp:
            present=fp.readlines()
        return present
    
    @classmethod
    def get_absent_data(self):
        with open('resources/absent.txt', 'r') as fp:
            absent=fp.readlines()
        return absent

for n in range(10000, 2000000, 10000):
    print('####  ' + str(n) + ' ####')
    false_count=0
    sb = Size_Bloom(n)
    for p in sb.present_data:
        sb.add(p)
    for a in sb.absent_data:
        val = sb.check(a)
        if val:
            false_count+=1
    percent_false=(false_count/len(sb.absent_data))*100
    print(str(percent_false) + '% are false positives: count is - ' + str(false_count))