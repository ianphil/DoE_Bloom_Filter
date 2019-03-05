#!/usr/bin/env python
import mmh3
import math
from bitarray import bitarray

class BloomFilter(object):
    def __init__(self, size, hash_passes):
        self.size = size
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(False)
        self.hash_passes = hash_passes
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        return iter(self.bit_array)

    def add(self, item):
        for i in range(self.hash_passes):
            h = mmh3.hash(item, i) % self.size
            self.bit_array[h] = True

    def __iadd__(self, item):
        self.add(item)
        return self

    def __contains__(self, item):
        digest=[]
        for i in range(self.hash_passes):
            h = mmh3.hash(item, i) % self.size
            present = self.bit_array[h]
            if not present:            
                return False
            else:
                digest.append(present)
                if len(digest) == self.hash_passes:
                    return True

class BloomFilterCalculator(object):

    def bit_array_size(self, n, p):
        '''
        m = bit array size
        n = number of items
        p = false positive probability
        '''
        m = -(n * math.log(p)) / (math.log(2)**2)
        return int(m)

    def hash_pass_count(self, m, n):
        '''
        m = bit array size
        n = number of items
        k = number of hash passes
        '''
        k = (m/n) * math.log(2)
        return int(k)

    def false_positive_probability(self, m, k, n):
        '''
        m = bit array size
        n = number of items
        k = number of hash passes
        p = false positive probability
        '''
        p = (1-(1-1/m)**(k*n))**k
        return float('{0:.4f}'.format(p))
