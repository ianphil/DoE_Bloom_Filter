#!/usr/bin/env python

# HYPO: Increase size will decrease FP
# HYPO: Increase hash pass will decrease FP
# HYPO: Minimize size and hash while maintaining low FP will increase spead

class Size_Bloom(object):
    def __init__(self, item_count):
        self.init_size=item_count
        self.present_data=self.get_present_data()
        self.absent_data=self.get_absent_data()
    
    @classmethod
    def get_present_data(self):
        with open('resources/present.txt', 'r') as fp:
            present=fp.readlines()
        return present
    
    @classmethod
    def get_absent_data(self):
        with open('resources/absent.txt', 'r') as fp:
            absent=fp.readlines()
        return absent