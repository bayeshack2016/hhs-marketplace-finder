#!/bin/env python

import json
import pymongo

def make_providers():

    with open('data/provider.json', 'r') as f:
        dat = json.load(f)

    # setup connections
    c = pymongo.MongoClient()

    for collection in ['plans', 'addresses', 'name', 'accepting']:
        for document_id, array in dat[collection].items():
            document = {'_id' : document_id, 'values' : array}
            c[database][collection].insert_one(document)

if __name__ == '__main__':
    make_providers()
