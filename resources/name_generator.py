#!/usr/bin/env python

family_file='familynames-usa-top1000.txt'
female_file='femalenames-usa-top1000.txt'
male_file='malenames-usa-top1000.txt'
username_file='usernames.txt'

# (female * family) + (male * family) = 2,000,000
# wc -l username.txt = 2,000,000

user_file=open(username_file, 'w')

with open(family_file) as fam_fp:
    fam_line = fam_fp.readline()
    while fam_line:
        with open(female_file) as f_fp:
            f_line = f_fp.readline()
            while f_line:
                f_user = f_line.strip().lower() + '.' + fam_line.lower()
                user_file.write(f_user)
                f_line = f_fp.readline()
        with open(male_file) as m_fp:
            m_line = m_fp.readline()
            while m_line:
                m_user = m_line.strip().lower() + '.' + fam_line.lower()
                user_file.write(m_user)
                m_line = m_fp.readline()
        fam_line = fam_fp.readline()

user_file.close()
