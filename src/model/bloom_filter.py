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
        item = item.strip()
        for i in range(self.hash_passes):
            h = mmh3.hash(item, i) % self.size
            self.bit_array[h] = True

    def __iadd__(self, item):
        self.add(item)
        return self

    def count(self):
        return self.bit_array.count()

    def check(self, item):
        digest=[]
        item = item.strip()
        for i in range(self.hash_passes):
            h = mmh3.hash(item, i) % self.size
            present = self.bit_array[h]
            if not present:            
                return False
            else:
                digest.append(present)
                if len(digest) == self.hash_passes:
                    return True

    def __contains__(self, item):
        return self.check(item)

class BloomFilterCalculator(object):

    def bit_array_size(self, n, p):
        '''
        input:
            n = number of items
            p = false positive probability
        output:
            m = bit array size
        '''

        m = -(n * math.log(p)) / (math.log(2)**2)
        return int(m)

    def hash_pass_count(self, m, n):
        '''
        input:
            m = bit array size
            n = number of items
        output:
            k = number of hash passes
        '''

        k = (m/n) * math.log(2)
        return int(k)

    def false_positive_probability(self, m, k, n):
        '''
        input:
            m = bit array size
            k = number of hash passes
            n = number of items
        output:
            p = false positive probability
        '''
        
        p = (1-(1-1/m)**(k*n))**k
        return float('{0:.4f}'.format(p))
