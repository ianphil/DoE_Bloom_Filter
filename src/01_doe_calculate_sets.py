#!/usr/bin/env python

from model.bloom_filter import BloomFilterCalculator

def test_false_positive_probability():
    calc = BloomFilterCalculator()
    p = calc.false_positive_probability(124, 4, 20)

def main():
    calc = BloomFilterCalculator()

    n = 10000
    p = 0.05

    m = calc.bit_array_size(n, p)
    msg = 'Bit Array size for 10,000 items with a 5% false positive probability: {}'.format(m)
    print(msg)

    k = calc.hash_pass_count(m, n)
    msg = 'Hash passes for 10,000 items with a {} sized bit array: {}'.format(m, k)
    print(msg)

if __name__ == '__main__':
    main()