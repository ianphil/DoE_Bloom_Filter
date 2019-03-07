#!/usr/bin/env python

from model.bloom_filter import BloomFilterCalculator

# These are the calculations to understand the right-size of the 
# factors that are controlable for Bloom Filters. We are given a number 
# of items and an acceptable false positive probability. Using these 
# factors, we are able to calculate the size of the bit array and the 
# amount of hash passes needed to optimize and balance the factors 
# against each other.
def main():
    calc = BloomFilterCalculator()

    # Number of items added to the Bloom Filter
    n = 10000

    # Probability of false positives
    p = 0.05

    # Size of bit array that will provide storage for the hashes
    m = calc.bit_array_size(n, p)
    msg = 'Bit Array size for 10,000 items with a 5% false positive probability: {}'.format(m)
    print(msg)

    # The amount of times we will hash the item
    k = calc.hash_pass_count(m, n)
    msg = 'Hash passes for 10,000 items with a {} sized bit array: {}'.format(m, k)
    print(msg)

if __name__ == '__main__':
    main()


# TODO: Slide to define m,n,p,k and formulas  