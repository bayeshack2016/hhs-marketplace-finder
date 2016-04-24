#!/bin/env python

import pymongo
import re

c = pymongo.MongoClient()

def split_name(name_string):
    name_string = name_string.strip()
    name_string = re.sub(r'\w+\.', '', name_string)
    fname = name_string.split()[0]
    lname = name_string.split()[-1] #we want to skip middle name if present
    return fname, lname

def get_plans(fname, lname):
    doctor_id = c['providers']['name'].find_one(
        {
        'values' :
            {
            'first' : fname,
            'last' : lname
            }
        }, {
        '_id' : 1
        }
    )
    return c['providers']['plans'].find_one(
        {
        '_id' : doctor_id
        },
        {
        'values' : 1
        }
    )

def get_locals(zip_code):
    return_list = []
    cursor = c['providers']['addresses'].find(
        {
            'values' : {
                '$elemMatch' : {'zip' : zip_code}
            }
        },{
        '_id' : 0
        }
    )
    for item in cursor:
        return_list.extend(item['values'])
    return return_list
