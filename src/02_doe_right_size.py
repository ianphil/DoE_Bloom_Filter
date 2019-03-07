#!/usr/bin/env python

from model.bloom_filter import BloomFilter
from model.users import PresentUsers, AbsentUsers

# Here we configure the bloom filter using optimal settings for 10,000 items.
# We then test using a list of absent users and display the results. Since we 
# have 1,000 absent users and an expected .05 false positive probability, then
# we should get 50 false positives. This simply proves that our calculations and
# bloom filter implementation is accurate. 
def main():
    # Present file contains 10,000 generated usernames that are added to the bloom filter.
    present_users_file = './src/resources/present.txt'

    # Absent file contains 1,000 generated usersnames that are not in the bloom filter.
    absent_users_file = './src/resources/absent.txt'

    # Read files into models
    present_users = PresentUsers(present_users_file)
    absent_users = AbsentUsers(absent_users_file)

    # Create bloom filter based on calculations for right-sizing to
    # 10,000 items and a 0.05 false positive rate.
    bloom_filter = BloomFilter(62352, 4)

    # Add present users to the bloom filter.
    for i in range(len(present_users)):
        bloom_filter += present_users[i]

    # Test for absent users and count the false positives.
    false_positive_count = 0
    for user in absent_users:
        if user in bloom_filter:
            false_positive_count += 1

    print('There are {} false positives for {} absent users, or {} false positive probability'
        .format(false_positive_count, len(absent_users), false_positive_count/len(absent_users)))

if __name__ == '__main__':
    main()