"""
Author: Aamir Zainulabadeen

CURRENTLY ONLY PULLS FIRST MONTH

Generate a date file to automate the webscraping of Prince articles.
The file is named 'dates.txt' in the top directory.

The command line arguments are 1: PATH and 2: year.
"""
import sys
import os

# format a day, s is either '/' or '_'
def formatDay(m, d, y, s):
    return m + s + d + s + y

def formatDir(m, d, y, s):
    return y + s + m + s + d

# generate properly formatted dates
# for each day in the year
def main():
    if len(sys.argv) < 3:
        print "BAD ARGUMENTS"
        return 0


    # pull out the arguments
    savePath = str(sys.argv[1])
    year = str(sys.argv[2])

    # months
    months = ['01']#, '02', '03', '04']
    base = ['01', '02', '03', '04', '05', '06', '07', '08', '09']
    dRange = range(10, 32)
    next = [str(d) for d in dRange]
    days = base + next


    with open("dates.txt", "w") as outF:
        for m in months:
            for d in days:
                #print formatDay(m, d, year, '/') + " " + formatDay(m, d, year, '_')
                outF.write(formatDay(m, d, year, '/') + " " + formatDir(m, d, year, '_') + "\n")


# run main
if __name__=="__main__":
    main()
