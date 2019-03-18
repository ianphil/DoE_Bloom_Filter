#!/usr/bin/env python

from model.bloom_filter import BloomFilter
from model.users import PresentUsers, AbsentUsers
import matplotlib.pyplot as plt 
import numpy as np
import math

# This is the last experiment, a 2 factorial designed experiment. The goal is to understand 
# the mass effect of each variable, but also the interaction between the to variables we control
# and how they affect the respons variable (false positives). 
def main():
    
    # Present file contains 10,000 generated usernames that are added to the bloom filter.
    present_users_file = './src/resources/present.txt'

    # Absent file contains 1,000 generated usersnames that are not in the bloom filter.
    absent_users_file = './src/resources/absent.txt'

    # Read files into models
    present_users = PresentUsers(present_users_file)
    absent_users = AbsentUsers(absent_users_file)

    # Loop over a specified range of ints to adjust both the bit array size
    # and the hash pass count for the bloom filter. M Range is 50,000 to 70,000 with 
    # a step of 10,000. This should surround the right sized value of 62352. k range is 3 to
    # 5 and also should surround the right sized value of 4.
    # TODO: O(n^2) - refactor to more be efficient using a memoization pattern.
    cnt_size = []
    cnt_passes = []
    cnt_fp = []
    for hash_count in range(3, 5):
        for bit_arr_size in range(50000, 70000, 10000):

            # Bloom filter with varying values for both hash passes and bit array sizes 
            # for 10,000 items
            bloom_filter = BloomFilter(bit_arr_size, hash_count)

            # Add present users to the bloom filter.
            for i in range(len(present_users)):
                bloom_filter += present_users[i]

            # Test for absent users and count the false positives.
            false_positive_count = 0
            for user in absent_users:
                if user in bloom_filter:
                    false_positive_count += 1

            cnt_fp.append(false_positive_count)
            cnt_passes.append(hash_count)
            cnt_size.append(bit_arr_size)

            print('There are {} false positives when bit array size is {} and hash count is {}'
                .format(false_positive_count, bit_arr_size, hash_count))

# TODO: Refactor into something else
    # Cube Plot
    plt.plot(cnt_passes, cnt_size, 'o')
    plt.xticks(ticks=[3, 4])
    plt.yticks(ticks=[50000, 60000])
    plt.xlabel('Hash Pass Count')
    plt.ylabel('Bit Array Size')
    plt.title('Cube Plot')
    for i in range(4):
        plt.text(cnt_passes[i], cnt_size[i], ' ' + str(cnt_fp[i]), size='15')

    # Hash Pass Main Effect + Plot
    hash_pass_x_axis = cnt_passes[:3:2]
    hash_pass_fp_3 = cnt_fp[:2]
    hash_pass_fp_4 = cnt_fp[2:4]
    hash_pass_y_axis = []
    hash_pass_y_axis.append(np.sum(hash_pass_fp_3)/len(hash_pass_fp_3))
    hash_pass_y_axis.append(np.sum(hash_pass_fp_4)/len(hash_pass_fp_4))
    mass_diff_hash = np.absolute(hash_pass_y_axis[0]-hash_pass_y_axis[1])
    print('The mass effect for hash passes is {}'.format(mass_diff_hash))

    plt.figure(2)
    plt.plot(hash_pass_x_axis, hash_pass_y_axis)
    plt.yticks(ticks=[40, 100])
    plt.xlabel('Hash Pass Count')
    plt.ylabel('False Positive Avg')
    plt.title('Hash Pass Count Mass Effect')

    # Bit Array Size Main Effect + Plot
    bit_size_x_axis = cnt_size[:2]
    bit_size_fp_5 = cnt_fp[:3:2]
    bit_size_fp_6 = cnt_fp[1:4:2]
    bit_size_y_axis = []
    bit_size_y_axis.append(np.sum(bit_size_fp_5)/len(bit_size_fp_5))
    bit_size_y_axis.append(np.sum(bit_size_fp_6)/len(bit_size_fp_6))
    mass_diff_size = np.absolute(bit_size_y_axis[0]-bit_size_y_axis[1])
    print('The mass effect for bit array size is {}'.format(mass_diff_size))

    plt.figure(3)
    plt.plot(bit_size_x_axis, bit_size_y_axis)
    plt.yticks(ticks=[40, 100])
    plt.xlabel('Bit Array Size Count')
    plt.ylabel('False Positive Avg')
    plt.title('Bit Array Size Mass Effect')
    

    # Hash Pass/Bit Array Size Interaction Effect + Plot
    interaction_fp_1 = [cnt_fp[0], cnt_fp[-1]]
    interaction_fp_2 = [cnt_fp[1], cnt_fp[-2]]
    interaction_effect = np.absolute((np.sum(interaction_fp_1)/len(interaction_fp_1))-(np.sum(interaction_fp_2)/len(interaction_fp_2)))
    print('The Hash Pass / Bit Array Size effect is {}'.format(interaction_effect))

    plt.figure(4)
    plt.plot(interaction_fp_1, '-o')
    plt.plot(interaction_fp_2, '-o')

    plt.show()


if __name__ == '__main__':
    main()


  