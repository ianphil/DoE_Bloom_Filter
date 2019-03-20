# Designing Experiments using Bloom Filters
In today’s computing landscape utility computing and layers of abstraction reduce the complexity of creating scientific, advanced decision, or prediction software. This leads to a lack of understanding how these work in modern computing. In this repo our focus is on the underlying data and factors that go into creating machine learning models. Most of the work creating an ML model is spent scrubbing the data and getting it into a shape that it can be processed. This data is then used to train a model. Due to the utility and ubiquity of computing resources today, there is not a lot of thought going into how the data is best used while training a model. 

Through a simple, statistically based approach to experimentation we can better understand the factors that make up our data. This will give better understanding to how and why our models are either working or failing. The advanced nature that makes up modern algorithms and computing infrastructure it takes to understand much of the work being done today, we will focus our work on Bloom Filters. This probabilistic data structure is very well understood and gives us a known target to demonstrate how to create experiments that can be applied to many of the problems that face us today. These experiments are only to explore the process of experimentation and not necessarily to learn anything new about this data structure.

![image](https://user-images.githubusercontent.com/17349002/54678757-32612a80-4adc-11e9-850c-211c114a9a35.png)

>Correlation doesn't imply causation, but it does waggle its eyebrows suggestively and gesture furtively while mouthing 'look over there'.

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

![image](https://user-images.githubusercontent.com/17349002/54603434-a76c2b80-4a1a-11e9-87f7-5566b7651c60.png)

```python
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
```

 2. Size of the bit array
    * Let bit array size be “m”

![image](https://user-images.githubusercontent.com/17349002/54603465-bd79ec00-4a1a-11e9-85fa-f20ca5c8a790.png)

```python
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
```

 3. Number of hash functions or passes
    * Let hash function pass count be “k”

![image](https://user-images.githubusercontent.com/17349002/54603488-d08cbc00-4a1a-11e9-83fc-af280592186f.png)

```python
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
```

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

![image](https://user-images.githubusercontent.com/17349002/54603350-75f36000-4a1a-11e9-908d-a6f8372e63f0.png)

The code snippet above is found in [03_doe_fat_hash.py](https://github.com/iphilpot/DoE_Bloom_Filter/blob/master/src/03_doe_fat_hash.py) where we are conducting a OFAT experiment varying only the count of hash passes used to insert items into the bloom filter’s bit array. The figure below is a graph of the effect this has on the response variable: false positives. From this we see that when all other variables are fixed, false positives are minimized at 4 and 6 hash passes. This is suspect because when other factors are changed, we may get different results and interactions are not detectable. 

## Factorial Experiment
The goal of a factorial experiment is to “turn the knobs” of all the factors being tested and understand the effect and interactions each have on one another. The major advantage is that using these techniques we can utilize all of the data gathered to determine how best to work with the factors when building machine learning models or solving problems considered complex.

For our Bloom Filter, we are designing a 2-factor factorial experiment. Our controllable variables will consist of the Bit Array size and Hash pass count. All other variables will be held constant using the right-size configuration for our bloom filter. I would like to point out that bloom filters and their factors are a known quantity. As mentioned previously, these experiments are only to explore the process of experimentation and not necessarily to learn anything new about this data structure.

```python
#!/usr/bin/env python

from model.bloom_filter import BloomFilter
from model.users import PresentUsers, AbsentUsers
import matplotlib.pyplot as plt 
import numpy as np
import math

# This is the last experiment, a 2 factorial designed experiment. The goal is to understand 
# the main effect of each variable, but also the interaction between the to variables we control
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
```

The code above is in the file [05_doe_fact_all.py](https://github.com/iphilpot/DoE_Bloom_Filter/blob/master/src/05_doe_fact_all.py) and will drive the experiment. Since we already have the answers to what the settings are for right-sized bloom filter, we establish the factor experimental levels so as to gain the greatest amount of information with the fewest number of experimental runs. For hash pass counts we use 3 and 4. For bit array size we use 50,000 and 60,000. For this experiment we will only do one pass. There is no variation in the response variable between runs, so we know the output is statistically significant. Otherwise we would employ additional techniques to assess if the results are statistically significant.

![image](https://user-images.githubusercontent.com/17349002/54603136-f1a0dd00-4a19-11e9-8300-1d66718f92f2.png)

The cube plot above shows a 2-factor experiment. The plot has each factor at different levels and each combination shown. This creates a 2-d square where a 3-factor experiment would create a cube. The different combinations for further analysis will be derived from this plot.

To understand the main effect that the hash pass counts have on our experiment we will take the average of these and plot them. The data from our cube plot would look something like:

![image](https://user-images.githubusercontent.com/17349002/54553383-73482a80-4988-11e9-960c-4d2044de22f7.png)

![image](https://user-images.githubusercontent.com/17349002/54603024-ad154180-4a19-11e9-8d5e-c4de373cec25.png)

The main effect for hash passes is 1.5

This is found by taking the averages of the two runs and finding the difference: ([83+58]/2)-([95+49]/2) = 1.5

![image](https://user-images.githubusercontent.com/17349002/54553468-a1c60580-4988-11e9-93dd-144b85aea89a.png)

![image](https://user-images.githubusercontent.com/17349002/54603261-3c225980-4a1a-11e9-8410-cf736fe8d924.png)

The main effect for bit array size is 35.5

Similarly, this is found by taking the averages of the two runs and finding the difference: ([83+95]/2)-([58+49]/2) = 35.5

From these two graphs we see that both effect the response variable, but that the bit array size has a more significant effect.

![image](https://user-images.githubusercontent.com/17349002/54553547-cf12b380-4988-11e9-9bb1-22e80b82bba1.png)

![image](https://user-images.githubusercontent.com/17349002/54603285-4d6b6600-4a1a-11e9-8a6d-e2c2125c8b04.png)

The Hash Pass / Bit Array Size interaction effect is 10.5

The hash pass / bit array size interaction effect is obtained by taking the average false positives from left to right diagonal: ([83+49]/2)-([58+95]/2) = 10.5

From this we see that there is an interaction between the two as we’d expect. 10.5 is considered significant and would direct further experimentation to focus on the interaction. Each factor has an effect, but they also depend on the level of other factors. From this we see that when 4 hash passes are deployed, false positives are minimized with a 60000 bit array. Using these values and knowledge, we can create further experiments to find the optimal settings for each factor. Adjusting the “knobs” in relation to the main and interaction effects found. 

## Conclusion
The idea for this study is not to use Bloom Filters for anything other than simply a data structure to experiment with. We could've used anything in its place, but it turned out to be a great example. And fun to learn about.

The main point is how we modeled the experiment, the results, and the findings they drove. Ultimately bit array size (m) is more important than hash passes (k) and the interaction of both (m + k) is very significant. This supports the known properties of Bloom filters.

Applying this to an ML model or complex problems, we can decide what are the more important factors and how they interact, or if there is no interaction between the factors. This gives us an efficient starting point for training models or writing algorithms. Ultimately, we can hypothesize that we can reduce overall training time and costs using this method. 

