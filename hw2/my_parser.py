import json
import sqlite3


"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"
bidders_array = []
sellers_array = []

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        users_array = []
        bids_array = []
        items_array = []
        for item in items:
            itemID = item['ItemID']
            item_array = []
            item_array.append(itemID)
            item_array.append(item['Name'])
            item_array.append(','.join(item['Category']))
            item_array.append(transformDollar(item['Currently']))
            item_array.append(transformDollar(item['First_Bid']))
            item_array.append(item['Number_of_Bids'])
            item_array.append(transformDttm(item['Started']))
            item_array.append(transformDttm(item['Ends']))
            item_array.append(item['Country'])
            item_array.append(item['Location'])
            if item['Description'] is not None:
                item_array.append(item['Description'].replace('"', ''))
            items_array.append(item_array)
            if item['Bids'] is not None:
                for current_bid in item['Bids']:
                    bid = current_bid['Bid']
                    bid_array = []
                    bid_array.append(itemID)
                    bid_array.append(bid['Bidder']['UserID'])
                    bid_array.append(transformDttm(bid['Time']))
                    bid_array.append(transformDollar(bid['Amount']))
                    bids_array.append(bid_array)
                    if bid['Bidder']['UserID'] not in bidders_array and bid['Bidder']['UserID'] not in sellers_array:
                        bidder_array = []
                        bidders_array.append(bid['Bidder']['UserID'])
                        bidder_array.append(bid['Bidder']['UserID'])
                        bidder_array.append(bid['Bidder']['Rating'])
                        if 'Country' in bid['Bidder']:
                            bidder_array.append(bid['Bidder']['Country'])
                        if 'Location' in bid['Bidder']:
                            bidder_array.append(bid['Bidder']['Location'])
                        users_array.append(bidder_array)
            if item['Seller']['UserID'] not in bidders_array and  item['Seller']['UserID'] not in sellers_array:
                seller_array = []
                sellers_array.append(item['Seller']['UserID'])
                seller_array.append(item['Seller']['UserID'])
                seller_array.append(item['Seller']['Rating'])
                if 'Country' in item:
                    seller_array.append(item['Country'])
                if 'Location' in item:
                    seller_array.append(item['Location'])
                users_array.append(seller_array)


        with open('Users.dat', 'w') as f:
            for user in users_array:
                f.write('|'.join(user) + '\n')

        with open('Bids.dat', 'w') as f:
            for bid in bids_array:
                f.write('|'.join(bid) + '\n')

        with open('Items.dat', 'w') as f:
            for item in items_array:
                f.write('|'.join(item) + '\n')


"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing")

if __name__ == '__main__':
    main(sys.argv)

#test