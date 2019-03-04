#!/usr/bin/env python

with open('absent.txt') as fp:
    absent=fp.readlines()

with open('present.txt') as fp:
    present=fp.readlines()

data = set(absent).intersection(present)
print(data)