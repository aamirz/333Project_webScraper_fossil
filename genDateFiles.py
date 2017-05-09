"""
Author: Aamir Zainulabadeen

CURRENTLY ONLY PULLS FIRST MONTH

Generate a date file to automate the webscraping of Prince articles.
The file is named 'dates.txt' in the top directory.

The command line arguments are 1: PATH and 2: year.
"""
import sys
import os
from datetime import date, datetime, timedelta

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

# print a range of dates
def main():
    for result in perdelta(date(2015, 01, 01), date(2017, 03, 31), timedelta(days=1)):
        print result.strftime("%Y_%m_%d") + "\t" + result.strftime("%m/%d/%Y")

# run main
if __name__=="__main__":
    main()
