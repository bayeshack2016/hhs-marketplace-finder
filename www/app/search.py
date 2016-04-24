#!/bin/env python

import re

def split_name(name_string):
    name_string = name_string.strip()
    name_string = re.sub(r'\w+\.', '', name_string)
    fname = name_string.split()[0]
    lname = name_string.split()[-1] #not 1 because we want to skip middle name
    return fname, lname

def get_plans(fname, lname):

def get_locals(plan):
