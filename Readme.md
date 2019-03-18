# Designing Experiments using Bloom Filters
In today’s computing landscape utility computing and layers of abstraction reduce the complexity of creating scientific, advanced decision, or prediction software. This leads to a lack of understanding how these work in modern computing. In this repo our focus is on the underlying data and factors that go into creating machine learning models. Most of the work creating an ML model is spent scrubbing the data and getting it into a shape that it can be processed. This data is then used to train a model. Due to the utility and ubiquity of computing resources today, there is not a lot of thought going into how the data is best used while training a model. 

Through a simple, statistically based approach to experimentation we can better understand the factors that make up our data. This will give better understanding to how and why are models are either working or failing. The advanced nature that makes up modern algorithms and computing infrastructure it takes to understand much of the work being done today, we will focus our work on Bloom Filters. This probabilistic data structure is very well understood and gives us a known target to demonstrate how to create experiments that can be applied to many of the problems that face us today. These experiments are only to explore the process of experimentation and not necessarily to learn anything new about this data structure.

## Bloom Filter
Bloom filters are a probabilistic data structure created in 1970 by Burton Bloom. It is used to test if an entity is found within a set. False Positive matches can and do occur, but false negatives do not. This means for the user that an item is possibly in the set, or it is not. Because of this, it has very specific use cases, but can drastically increase the speed or scale of a system ([Wikipedia](https://en.wikipedia.org/wiki/Bloom_filter)).

### Bloom Filter Internals
An empty bloom filter is a bit array of size “m” all set to zero. 

![image](https://user-images.githubusercontent.com/17349002/54532905-5d723f80-495f-11e9-9049-d3958751cd72.png)

When an item is added it is hashed “k” number of times. In this example k = 3.

![image](https://user-images.githubusercontent.com/17349002/54532982-8abeed80-495f-11e9-98aa-2c0448e870c2.png)

More items go through the same process.

![image](https://user-images.githubusercontent.com/17349002/54533045-ac1fd980-495f-11e9-868c-16da33c643e9.png)

Finally, when a look up is done, some items can cause false positives due to collisions in hash functions.

![image](https://user-images.githubusercontent.com/17349002/54533077-bd68e600-495f-11e9-876e-31c50cd1063e.png)

### Bloom Filter Code

```python
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
```

The code above, [bloom_filter.py](https://github.com/iphilpot/DoE_Bloom_Filter/blob/master/src/model/bloom_filter.py), shows both how to insert items (`add` method) and how to query for items (`check` method). These are referenced by the `__iadd__` and `__contains__` or special methods in python. This is to follow pythonic convention and enable code reuse.

### Bloom Filter Factors
There are three main factors we can use to efficiently and effectively store and test for items in a set using Bloom Filters.
 1. Probability of false positives
    * Let false positives be “p”

![image](https://user-images.githubusercontent.com/17349002/54538296-66b4d980-496a-11e9-8af5-7d4fcd6c7c09.png)

![image](https://user-images.githubusercontent.com/17349002/54538331-73393200-496a-11e9-885b-c743925caa77.png)

 2. Size of the bit array
    * Let bit array size be “m”

![image](https://user-images.githubusercontent.com/17349002/54538446-a380d080-496a-11e9-8a6b-7bba41332cbe.png)

![image](https://user-images.githubusercontent.com/17349002/54538457-a67bc100-496a-11e9-9089-cce953a9e62e.png)

 3. Number of hash functions or passes
    * Let hash function pass count be “k”

![image](https://user-images.githubusercontent.com/17349002/54538548-d32fd880-496a-11e9-9a81-9f9cbc70c068.png)

![image](https://user-images.githubusercontent.com/17349002/54538556-d5923280-496a-11e9-8ff6-b9168b555eb6.png)

These equations are used to understand the settings needed to configure a bloom filter to store “x” number of items ([GeeksforGeeks](https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/)).

Another factor that we are able to control is the type of hash function used. Our experiments hold this constant using the `mmh3` pip package to provide this functionality.

## Description of Variables in Experiments
For our experiment we will be inserting 10,000 items (usernames) into our bloom filter. Using the above equations, we can right size our bloom filter with the following factors:
1.	10,000 Items inserted
2.	1,000 Absent items to test with
3.	Bit array size: 62352
4.	Hash pass count: 4
5.	Target false positive rate: 0.05

```python
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
```

The code above is found in: [02_doe_right_size.py](https://github.com/iphilpot/DoE_Bloom_Filter/blob/master/src/02_doe_right_size.py). The result is as expected, 50 false positive items returned. 

## One Factor at a Time Experiments
A common strategy of experimentation is One Factor at a Time (OFAT) type of experiments. The experimenter selects a starting point, or baseline, for one of the controllable factors then varying it while holding all other factors constant. After all the experiments are completed a set of graphs are made to show how the response variable changes. “The major disadvantage of the OFAT strategy is that it fails to consider any possible interaction between the factors.” ([Montgomery, D. C.](https://www.wiley.com/en-us/Design+and+Analysis+of+Experiments%2C+9th+Edition-p-9781119113478)).

An interaction causes the response variable to differ when testing a controllable variable at varied levels of the other controllable variables. Understanding this and the effect that this interaction has on our experiments, will help us focus on the factors that are most important when training machine learning models or solving complex problems using other data analysis methods.

```python
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
```

![image](https://user-images.githubusercontent.com/17349002/54539115-f14a0880-496b-11e9-8c37-958d6dc7c45a.png)

The code snippet above is found in [03_doe_fat_hash.py](https://github.com/iphilpot/DoE_Bloom_Filter/blob/master/src/03_doe_fat_hash.py) where we are conducting a OFAT experiment varying only the count of hash passes used to insert items into the bloom filter’s bit array. The figure below is a graph of the effect this has on the response variable: false positives. We see that there is not very much information to be gleaned from this type of experiment.

## Factorial Experiment
The goal of a factorial experiment is to “turn the knobs” of all the factors being tested and understand the effect and interactions each have on one another. The major advantage is that using these techniques we can utilize all of the data gathered to determine how best to work with the factors when building machine learning models or solving problems considered complex.

For our Bloom Filter, we are designing a 2-factor factorial experiment. Our controllable variables will consist of the Bit Array size and Hash pass count. All other variables will be held constant using the right-size configuration for our bloom filter. I would like to point out that bloom filters and their factors are a known quantity. As mentioned previously, these experiments are only to explore the process of experimentation and not necessarily to learn anything new about this data structure.
