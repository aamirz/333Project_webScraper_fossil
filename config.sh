# Aamir Zainulabadeen
# Configuration for Prowler's webscraper
#

#!/bin/bash

# format our database
python formatDB.py

# make our data directories for each publication
DIR='./data'
mkdir $DIR
mkdir $DIR/prince
mkdir $DIR/nass
mkdir $DIR/tigerMag

# the old publication archive pullings
DIR='./oldData'
mkdir $DIR
mkdir $DIR/prince
mkdir $DIR/nass
mkdir $DIR/tigerMag

exit 0

