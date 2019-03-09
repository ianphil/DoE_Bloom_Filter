#!/usr/bin/env python

from model.bloom_filter import BloomFilter
from model.users import PresentUsers, AbsentUsers
import matplotlib.pyplot as plt 

# This is the second experiment. We are focused on only one factor m (bit array).
# We hold the size of k (hash passes) constant and only adjust m over a range of 
# 10,000 to 90,000 and show how many false positives we receive. This doesn't 
# provide very much insight into how bloom filters work, because we don't understand
# how the constant variables affect the response variable.
def main():
    # Present file contains 10,000 generated usernames that are added to the bloom filter.
    present_users_file = './src/resources/present.txt'

    # Absent file contains 1,000 generated usersnames that are not in the bloom filter.
    absent_users_file = './src/resources/absent.txt'

    # Read files into models
    present_users = PresentUsers(present_users_file)
    absent_users = AbsentUsers(absent_users_file)

    # Loop over a specified range of ints to adjust the size of the bit array for 
    # the bloom filter. Range is 10,000 to 90,000 with a step of 10,000.
    cnt_size = []
    cnt_fp = []
    for bit_arr_size in range(10000, 90000, 10000):

        # Bloom filter right sized to hash passes for 10,000 items, but adjusted the
        # bit array size
        bloom_filter = BloomFilter(bit_arr_size, 4)

        # Add present users to the bloom filter.
        for i in range(len(present_users)):
            bloom_filter += present_users[i]

        # Test for absent users and count the false positives.
        false_positive_count = 0
        for user in absent_users:
            if user in bloom_filter:
                false_positive_count += 1

        # Add results to list for graph
        cnt_size.append(bit_arr_size)
        cnt_fp.append(false_positive_count)

        print('There are {} false positives when bit array size is {}'
            .format(false_positive_count, bit_arr_size))

    # Create and show graph
    plt.plot(cnt_size, cnt_fp)
    plt.show()

if __name__ == '__main__':
    main()