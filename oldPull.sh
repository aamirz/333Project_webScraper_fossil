# Aamir Zainulabadeen
# oldPull.sh
# pull all old prince articles

# TWO COMMAND LINE ARGUMENTS
# FIRST IS THE DAY IN "YYYY_MM_DD"
# SECOND IS THE DAY IN "MM/DD/YYYY"

#!/bin/bash

TODAY=$1
DAY=$2
PARDIR="./data"
#TODAY="YYYY_MM_DD"
#DAY="MM/DD/YYYY"
SAVEME="./data/prince/${TODAY}"
mkdir $SAVEME

echo "PULLING OLD STUFF"
echo $DAY
python pullOldPrince.py $PARDIR $DAY

# get the number of articles pulled
N="$(ls "${SAVEME}" | wc -l)"
echo $N
# post all of the articles
python postScrapedArticles.py $SAVEME $N $TODAY

# now remove all of the articles
rm -rf "${SAVEME}"

exit 0
