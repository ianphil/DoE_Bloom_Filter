#!/usr/bin/env python

from model.bloom_filter import BloomFilter
from model.users import PresentUsers, AbsentUsers
import matplotlib.pyplot as plt 

# This is the first of the experiments. We are focused on only one factor k (hash passes).
# We hold the size of m (bit array) constant and only adjust k over a range of 1-9 and show 
# how many false positives we receive. This doesn't provide very much insight into how bloom
# filters work, because we don't understand how the constant variables affect the response 
# variable. 
def main():
    # Present file contains 10,000 generated usernames that are added to the bloom filter.
    present_users_file = './src/resources/present.txt'

    # Absent file contains 1,000 generated usersnames that are not in the bloom filter.
    absent_users_file = './src/resources/absent.txt'

    # Read files into models
    present_users = PresentUsers(present_users_file)
    absent_users = AbsentUsers(absent_users_file)

    # Loop over a specified range of ints to adjust how many hash passes the bloom filter
    # performs for each item added.
    cnt_passes = []
    cnt_fp = []
    for hash_count in range(1, 10):

        # Bloom filter right sized to bit array size for 10,000 items, but adjusted hash
        # passes
        bloom_filter = BloomFilter(62352, hash_count)

        # Add present users to the bloom filter.
        for i in range(len(present_users)):
            bloom_filter += present_users[i]

        # Test for absent users and count the false positives.
        false_positive_count = 0
        for user in absent_users:
            if user in bloom_filter:
                false_positive_count += 1

        # Add result for graph
        cnt_passes.append(hash_count)
        cnt_fp.append(false_positive_count)

        print('There are {} false positives when hash pass count is {}'
            .format(false_positive_count, hash_count))

    # Create and show graph
    plt.plot(cnt_passes, cnt_fp)
    plt.show()
        

if __name__ == '__main__':
    main()