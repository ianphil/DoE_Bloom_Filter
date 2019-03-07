#!/usr/bin/env python

from model.bloom_filter import BloomFilter
from model.users import PresentUsers, AbsentUsers

def main():
    present_users_file = './src/resources/present.txt'
    absent_users_file = './src/resources/absent.txt'
    present_users = PresentUsers(present_users_file)
    absent_users = AbsentUsers(absent_users_file)

    for hash_count in range(3, 5):
        for bit_arr_size in range(50000, 70000, 10000):
            bloom_filter = BloomFilter(bit_arr_size, hash_count)

            for i in range(len(present_users)):
                bloom_filter += present_users[i]

            false_positive_count = 0
            for user in absent_users:
                if user in bloom_filter:
                    false_positive_count += 1

            print('There are {} false positives when bit array size is {} and hash count is {}'
                .format(false_positive_count, bit_arr_size, hash_count))

if __name__ == '__main__':
    main()


  