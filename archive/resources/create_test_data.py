#!/usr/bin/env python
from random import shuffle

with open('usernames.txt') as fp:
    usernames = fp.readlines()
shuffle(usernames)

username_present=usernames[:10000]
username_absent=usernames[10000:11000]

with open('present.txt', 'w') as fp:
    fp.writelines(username_present)

with open('absent.txt', 'w') as fp:
    fp.writelines(username_absent)
