#!/usr/bin/env python

from model.bloom_filter import BloomFilter
from model.users import PresentUsers, AbsentUsers

def main():
    present_users_file = './src/resources/present.txt'
    absent_users_file = './src/resources/absent.txt'
    present_users = PresentUsers(present_users_file)
    absent_users = AbsentUsers(absent_users_file)

    for hash_count in range(1, 10):
        bloom_filter = BloomFilter(62352, hash_count)

        for i in range(len(present_users)):
            bloom_filter += present_users[i]

        false_positive_count = 0
        for user in absent_users:
            if user in bloom_filter:
                false_positive_count += 1

        print('There are {} false positives when hash pass count is {}'
            .format(false_positive_count, hash_count))

if __name__ == '__main__':
    main()