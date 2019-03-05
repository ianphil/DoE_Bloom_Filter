#!/usr/bin/env python

class PresentUsers(object):
    def __init__(self, file_name):
        self._usernames = self.get_present_data(file_name)

    def __len__(self):
        return len(self._usernames)

    def __getitem__(self, position):
        return self._usernames[position]

    @classmethod
    def get_present_data(self, file_name):
        with open(file_name, 'r') as fp:
            present=fp.readlines()
        return present

class AbsentUsers(object):
    def __init__(self, file_name):
        self._usernames = self.get_absent_data(file_name)

    def __len__(self):
        return len(self._usernames)

    def __getitem__(self, position):
        return self._usernames[position]

    @classmethod
    def get_absent_data(self, file_name):
        with open(file_name, 'r') as fp:
            absent=fp.readlines()
        return absent