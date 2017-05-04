# pullToday.sh
#
# Author: Aamir Zainulabadeen
#
#
# Pull today's contents for all publications. 
# Save them all to the data/ directory. Then removes all 
# the data after posting. 
#

# launch shell
#!/bin/bash

# cron preamble
cd ~
cd prowler_webScraper/

# get today's date 
TODAY="$(date "+%Y_%m_%d")"
DAY="$(date "+%m/%d/%Y")"
#DAY="04/13/2017"
#TODAY="2017_04_13"

PUBDIRS=(./data/*)

# make the date directories for each publication 
for file in "${PUBDIRS[@]}"
do 
mkdir "${file}/${TODAY}"
done

# grab all of today's articles
python getTodaysArticles.py "./data" $DAY

# post all of today's articles, generate a count
for file in "${PUBDIRS[@]}"
do
# get the number of articles 
echo "${file}"
N="$(ls "${file}/${TODAY}/" | wc -l)"
echo $N
python postScrapedArticles.py "${file}/${TODAY}" $N $TODAY
done

# now remove all of data 
for file in "${PUBDIRS[@]}"
do
# now remove the parent directory and all contents
echo "removing ${file}/${TODAY}"
#rm -rf "./${file}/${TODAY}"
done

# success
exit 0
