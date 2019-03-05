#!/usr/bin/env python

import mmh3
from bitarray import bitarray

# HYPO: Size and hash pass count affect speed

class Bloom(object):
    def __init__(self, item_count, hash_pass_count):
        self.size=item_count
        self.hash_pass=hash_pass_count
        self.present_data=self.get_present_data()
        self.absent_data=self.get_absent_data()
        self.ba=bitarray(self.size)
        self.ba.setall(False)

    def add(self, item):
        for i in range(self.hash_pass):
            h=mmh3.hash(item, i)%self.size
            self.ba[h]=True

    def check(self, item):
        digest=[]
        for i in range(self.hash_pass):
            a_hash=mmh3.hash(item, i)%self.size
            a_present=self.ba[a_hash]
            digest.append(a_present)
            if not a_present:            
                return False
            else:
                if len(digest) == self.hash_pass:
                    return True

    @classmethod
    def get_present_data(self):
        with open('../resources/present.txt', 'r') as fp:
            present=fp.readlines()
        return present
    
    @classmethod
    def get_absent_data(self):
        with open('../resources/absent.txt', 'r') as fp:
            absent=fp.readlines()
        return absent

for s in range(10000, 30000, 10000):
    for h in range(1,3):
        false_count=0
        sb = Bloom(s, h)
        for p in sb.present_data:
            sb.add(p)
        for a in sb.absent_data:
            val = sb.check(a)
            if val:
                false_count+=1
        print(str(s) + ',' + str(h) + ',' + str(false_count))


# def __repr__(self):
#     return 'BloomFilter(ideal_num_elements_n=%d, error_rate_p=%f, num_bits_m=%d)' % (
#         self.ideal_num_elements_n,
#         self.error_rate_p,
#         self.num_bits_m,
#     )